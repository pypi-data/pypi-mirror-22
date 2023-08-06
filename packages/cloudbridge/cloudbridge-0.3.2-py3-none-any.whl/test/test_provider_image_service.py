import uuid
from cloudbridge.providers.interfaces import MachineImageState
from test.helpers import ProviderTestBase
import test.helpers as helpers


class CloudImageServiceTestCase(ProviderTestBase):

    def __init__(self, methodName, provider):
        super(CloudImageServiceTestCase, self).__init__(
            methodName=methodName, provider=provider)

    def test_create_and_list_image(self):
        """
        Create a new image and check whether that image can be listed.
        This covers waiting till the image is ready, checking that the image
        name is the expected one and whether list_images is functional.
        """
        instance_name = "CBImageTest-{0}-{1}".format(
            self.provider.name,
            uuid.uuid4())
        test_instance = helpers.get_test_instance(self.provider, instance_name)
        with helpers.exception_action(lambda: test_instance.terminate()):
            name = "CBUnitTestListImg-{0}".format(uuid.uuid4())
            test_image = test_instance.create_image(name)
            with helpers.exception_action(lambda: test_image.delete()):
                test_image.wait_till_ready(interval=helpers.TEST_WAIT_INTERVAL)
                images = self.provider.images.list_images()
                found_images = [image for image in images
                                if image.name == name]
                self.assertTrue(
                    len(found_images) == 1,
                    "List images does not return the expected image %s" %
                    name)
                test_image.delete()
                test_image.wait_for(
                    [MachineImageState.UNKNOWN],
                    terminal_states=[MachineImageState.ERROR],
                    interval=helpers.TEST_WAIT_INTERVAL)
            # TODO: Images take a long time to deregister on EC2. Needs
            # investigation
#                 images = self.provider.images.list_images()
#                 found_images = [image for image in images
#                                 if image.name == name]
#                 self.assertTrue(
#                     len(found_images) == 0,
#                     "Image %s should have been deleted but still exists." %
#                     name)
