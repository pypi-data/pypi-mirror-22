from opal.core.test import OpalTestCase
from opal.tests import models as test_models

from pathway import Step
from pathway.steps import InitializationError


class StepTestCase(OpalTestCase):
    def test_to_dict_model_passed_in(self):
        step_dict = Step(model=test_models.Colour).to_dict()
        self.assertEqual(
            step_dict["display_name"], "Colour",
        )
        self.assertEqual(
            step_dict["icon"], "fa fa-comments"
        )
        self.assertEqual(
            step_dict["api_name"], "colour"
        )
        self.assertEqual(
            step_dict["model_api_name"], "colour"
        )

    def test_to_dict_args_passed_in(self):
        step_dict = Step(
            display_name="Some Step",
            icon="fa fa-some-step",
            api_name="some_step",
            model_api_name="some_model_api_step",
            template="some_template.html"
        ).to_dict()
        self.assertEqual(
            step_dict["display_name"], "Some Step",
        )
        self.assertEqual(
            step_dict["icon"], "fa fa-some-step"
        )
        self.assertEqual(
            step_dict["api_name"], "some_step"
        )
        self.assertEqual(
            step_dict["model_api_name"], "some_model_api_step"
        )

    def test_arguments_passed_in_overide_model(self):
        step_dict = Step(
            model=test_models.Colour,
            display_name="Some Step",
            icon="fa fa-some-step",
            api_name="some_step",
            model_api_name="some_model_api_step",
            template="some_template.html"
        ).to_dict()
        self.assertEqual(
            step_dict["display_name"], "Some Step",
        )
        self.assertEqual(
            step_dict["icon"], "fa fa-some-step"
        )
        self.assertEqual(
            step_dict["api_name"], "some_step"
        )
        self.assertEqual(
            step_dict["model_api_name"], "some_model_api_step"
        )

    def test_no_display_name(self):
        with self.assertRaises(InitializationError) as er:
            Step(
                template="some_template.html"
            )
        self.assertEqual(
            str(er.exception), "a step needs either a display_name or a model"
        )

    def test_no_template(self):
        with self.assertRaises(InitializationError) as er:
            Step(
                display_name="no template"
            )
        self.assertEqual(
            str(er.exception), "a step needs either a template or a model"
        )
