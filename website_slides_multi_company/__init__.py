from . import models


def post_init_hook(env):
    """Assign existing courses to the company of their website.

    Courses without a website are left without a company so that they stay
    visible in every company, as they were before installing this module.
    """
    channels = env["slide.channel"].with_context(active_test=False).search([])
    for website, website_channels in channels.grouped("website_id").items():
        website_channels.company_id = website.company_id
