{% extends "admin/email/macros.html.tpl" %}
{% block language %}en{% endblock %}
{% block background_color %}#edece4{% endblock %}
{% block font_color %}#4d4d4d{% endblock %}
{% block font_size %}14px{% endblock %}
{% block font_family %}-apple-system, 'BlinkMacSystemFont', 'Segoe UI','Open Sans',Helvetica,Arial,sans-serif{% endblock %}
{% block line_height %}22px{% endblock %}
{% block content_width %}520px{% endblock %}
{% block html %}
    <!DOCTYPE html>
    <html lang="{{ self.language() }}">
    <head>
        {% block head %}
            <title>{% block title %}{% endblock %}</title>
            <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
            <style>
                p {
                    color: {{ self.font_color() }};
                    font-family: {{ self.font_family() }};
                    font-size: {{ self.font_size() }};
                    line-height: {{ self.line_height() }};
                    margin: 14px 0px 14px 0px;
                }
            </style>
        {% endblock %}
    </head>
    <body style="font-family:{{ self.font_family() }};font-size:{{ self.font_size() }};line-height:{{ self.line_height() }};color:{{ self.font_color() }};text-align:left;padding:0px 0px 0px 0px;margin:0px 0px 0px 0px;" bgcolor="{{ self.background_color() }}">
        {% block metadata %}{% endblock %}
        <div class="container" style="background-color:{{ self.background_color() }};margin:0px auto 0px auto;padding:48px 0px 48px 0px;" bgcolor="{{ self.background_color() }}">
            <div style="background-color:#ffffff;width:{{ self.content_width() }};margin:0px auto 0px auto;padding:42px 72px 42px 72px;border:1px solid #d9d9d9;">
                {% block logo %}{% endblock %}
                <div class="content">
                    {{ h1(self.title()) }}
                    {% block content %}{% endblock %}
                </div>
                <div class="footer" style="font-size:10px;line-height:16px;text-align:right;margin-top: 48px;">
                    &copy; {{ owner.copyright|default(copyright, True)|default("2014-2017 Hive Solutions", True) }} &middot; {{ "All rights reserved"|locale }}<br/>
                </div>
            </div>
        </div>
    </body>
    </html>
{% endblock %}
