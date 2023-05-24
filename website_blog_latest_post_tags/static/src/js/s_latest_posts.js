odoo.define(
    "website_blog_blogs_snippet.s_latest_posts_frontend_inherit",
    function (require) {
        "use strict";

        var core = require("web.core");
        var publicWidget = require("web.public.widget");
        require("website_blog.s_latest_posts_frontend");
        var _t = core._t;

        publicWidget.registry.js_get_posts.include({
            /**
             * @override
             */
            start: function () {
                var self = this;
                const data = self.$target[0].dataset;
                const promoted = data.promoted === "true" || false;
                const limit = parseInt(data.postsLimit, 20) || 4;
                const columns = parseInt(data.postsColumns, 20) || 3;
                const blogID = parseInt(data.filterByBlogId, 20);
                // Compatibility with old template xml id
                if (
                    data.template &&
                    data.template.endsWith(".s_latest_posts_big_orizontal_template")
                ) {
                    data.template = "website_blog.s_latest_posts_horizontal_template";
                }
                const template =
                    data.template || "website_blog.s_latest_posts_list_template";
                const loading = data.loading === "true";
                const order = data.order || "published_date desc";

                // Compatibility with db that saved content inside by mistake
                this.$target.empty();
                // Prevent user edition
                this.$target.attr("contenteditable", "False");

                var domain = [];
                if (blogID) {
                    domain.push(["blog_id", "=", blogID]);
                }
                if (order.includes("visits")) {
                    domain.push(["visits", "!=", false]);
                }
                if (promoted) {
                    domain.push(["is_promoted", "=", true]);
                }

                var prom = new Promise(function (resolve) {
                    self._rpc({
                        route: "/blog/render_latest_posts",
                        params: {
                            template: template,
                            domain: domain,
                            limit: limit,
                            order: order,
                            columns: columns,
                        },
                    })
                        .then(function (posts) {
                            var $posts = $(posts).filter(".s_latest_posts_post");
                            if (!$posts.length) {
                                self.$target.append(
                                    $("<div/>", {class: "col-md-6 offset-md-3"}).append(
                                        $("<div/>", {
                                            class: "alert alert-warning alert-dismissible text-center",
                                            text: _t(
                                                "No blog post was found. Make sure your posts are published."
                                            ),
                                        })
                                    )
                                );
                                resolve();
                            }

                            if (loading) {
                                // Perform an intro animation
                                self._showLoading($posts);
                            } else {
                                self.$target.html($posts);
                            }
                            resolve();
                        })
                        .guardedCatch(function () {
                            if (self.editableMode) {
                                self.$target.append(
                                    $("<p/>", {
                                        class: "text-danger",
                                        text: _t(
                                            "An error occured with this latest posts block. If the problem persists, please consider deleting it and adding a new one"
                                        ),
                                    })
                                );
                            }
                            resolve();
                        });
                });
                return Promise.all([prom]);
            },
        });
    }
);
