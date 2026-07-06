import {BaseOptionComponent} from "@html_builder/core/utils";
import {DEFAULT} from "@html_builder/utils/option_sequence";
import {Plugin} from "@html_editor/plugin";
import {withSequence} from "@html_editor/utils/resource";
import {_t} from "@web/core/l10n/translation";
import {registry} from "@web/core/registry";

export class CoursesPageOption extends BaseOptionComponent {
  static template = "website_slides_settings.CoursesPageOption";
  static selector = "main:has(.o_wslides_course_main)";
  static title = _t("Course Page");
  static groups = ["website.group_website_designer"];
  static editableOnly = false;
}

export class CoursesPageOptionPlugin extends Plugin {
  static id = "coursesPageOption";
  resources = {
    builder_options: [withSequence(DEFAULT, CoursesPageOption)],
  };
}

registry
  .category("website-plugins")
  .add(CoursesPageOptionPlugin.id, CoursesPageOptionPlugin);
