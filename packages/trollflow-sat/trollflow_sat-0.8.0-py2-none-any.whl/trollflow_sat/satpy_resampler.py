"""Classes for generating image composites for Trollflow based
Trollduction using satpy"""

import logging
import time

import yaml

from trollflow.workflow_component import AbstractWorkflowComponent
from trollflow_sat import utils


class Resampler(AbstractWorkflowComponent):

    """Creates resampled local area scenes."""

    logger = logging.getLogger("Resampler")

    def __init__(self):
        super(Resampler, self).__init__()

    def pre_invoke(self):
        """Pre-invoke"""
        pass

    def invoke(self, context):
        """Invoke"""
        # Set locking status, default to False
        self.use_lock = context.get("use_lock", False)
        self.logger.debug("Locking is used in resampler: %s",
                          str(self.use_lock))
        if self.use_lock:
            self.logger.debug("Compositor acquires lock of previous "
                              "worker: %s", str(context["prev_lock"]))
            utils.acquire_lock(context["prev_lock"])

        glbl = context["content"]
        with open(context["product_list"], "r") as fid:
            product_config = yaml.load(fid)

        # Handle config options
        kwargs = {}

        kwargs['precompute'] = context.get('precompute', False)
        self.logger.debug("Setting precompute to %s",
                          str(kwargs['precompute']))

        kwargs['nprocs'] = context.get('nprocs', 1)
        self.logger.debug("Using %d CPUs for resampling.", kwargs['nprocs'])

        kwargs['resampler'] = context.get('proj_method', "nearest")
        self.logger.debug(
            "Using resampling method: '%s'.", kwargs['resampler'])
        try:
            area = glbl.info['area'].area_id
            area_config = product_config["product_list"][area]
            kwargs['radius_of_influence'] = area_config.get("srch_radius",
                                                            context["radius"],
                                                            10000.)
        except (AttributeError, KeyError):
            kwargs['radius_of_influence'] = 10000.

        if kwargs['radius_of_influence'] is None:
            self.logger.debug("Using default search radius.")
        else:
            self.logger.debug("Using search radius %d meters.",
                              int(kwargs['radius_of_influence']))

        prod_list = product_config["product_list"]
        for area_id in prod_list:
            # Set lock if locking is used
            if self.use_lock:
                self.logger.debug("Resampler acquires own lock %s",
                                  str(context["lock"]))
                utils.acquire_lock(context["lock"])
            # if area_id not in glbl.info["areas"]:
            #     utils.release_locks([context["lock"]])
            #     continue

            # Reproject only needed channels
            dataset_names = utils.get_satpy_area_composite_names(
                product_config, area_id)
            dataset_ids = [ds_id for ds_id in glbl.datasets.keys()
                           if ds_id.name in dataset_names]
            if area_id == "satproj":
                self.logger.info("Using satellite projection")
                lcl = glbl
            else:
                self.logger.info("Resampling time slot %s to area %s",
                                 glbl.info["start_time"], area_id)
                lcl = glbl.resample(area_id, datasets=dataset_ids,
                                    **kwargs)
            lcl.info["product_config"] = product_config
            lcl.info["area_id"] = area_id
            lcl.info["products"] = prod_list[area_id]['products']
            lcl.info["dataset_ids"] = dataset_ids
            self.logger.debug("Inserting lcl (area: %s, start_time: %s) "
                              "to writer's queue",
                              area_id, str(lcl.info["start_time"]))
            context["output_queue"].put(lcl)
            del lcl
            lcl = None

            if utils.release_locks([context["lock"]]):
                self.logger.debug("Resampler releases own lock %s",
                                  str(context["lock"]))
                # Wait 1 second to ensure next worker has time to acquire the
                # lock
                time.sleep(1)

        # Wait until the lock has been released downstream
        if self.use_lock:
            utils.acquire_lock(context["lock"])
            utils.release_locks([context["lock"]])

        # After all the items have been processed, release the lock for
        # the previous step
        utils.release_locks([context["prev_lock"]], log=self.logger.debug,
                            log_msg="Resampler releses lock of previous " +
                            "worker: %s" % str(context["prev_lock"]))

    def post_invoke(self):
        """Post-invoke"""
        pass
