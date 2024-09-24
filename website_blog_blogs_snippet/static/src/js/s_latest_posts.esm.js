/** @odoo-module **/

import DynamicSnippetBlogPosts from "@website_blog/snippets/s_blog_posts/000";
import publicWidget from "@web/legacy/js/public/public_widget";

const DynamicSnippetBlogPostsPromoted = DynamicSnippetBlogPosts.extend({
    selector: ".s_dynamic_snippet_blog_posts",
    disabledInEditableMode: false,

    _getSearchDomain: function () {
        const searchDomain = this._super.apply(this, arguments);

        const data = self.$target[0].dataset;
        const promoted = data.promoted === "true" || false;

        const filterByBlogId = parseInt(this.$el.get(0).dataset.filterByBlogId);

        if (promoted && filterByBlogId >= 0) {
            searchDomain.push(["is_promoted", "=", true]);
        }

        return searchDomain;
    },
});

publicWidget.registry.blog_posts = DynamicSnippetBlogPostsPromoted;
export default DynamicSnippetBlogPostsPromoted;
