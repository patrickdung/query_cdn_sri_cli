Python script faster and safer use of CDN resources
---------------------------------------------------

This Python script queries two major CDN services (CDNJS and jsDelivr only).
It is similar to the [Pelican plugin](https://github.com/patrickdung/pelican_cdn_sri)

That plugin made use of global settings or global parameters so that the article/pages/templates
could reference the JINJA2 variables. This script does not same thing but use a different approach.
Instead of using Pelican generators/plugin framework. This script is designed to run
before running Pelican to generate static page. This script read an INI file and query the CDN,
then it generate a Pelican parameter file. Users then import the parameter file in their Pelican
config. Then the CDN_SRI parameters could be used. It use a different appoarch and the output
of the script could be used in other SSG or applications.

Also, this script supports use of either css or js file only.
The user provide information about which application and the version
that they want to use. The script queries the API of the CDN and
return a code block that could be used in the Pelican template.
The code block would include the SRI hash.
This save time for the users and is secure than just using the latest version
of an application and do not use SRI.

This script references several Pelican plugins. So this script
would be in AGPLv3.

- [Pelican Plugins](https://github.com/getpelican/pelican-plugins/)
- [pelican-webmention](https://github.com/drivet/pelican-webmention)
- [webmention_static_kappa](https://github.com/kappa-wingman/webmention_static_kappa)

How to use this script
----------------------

- Put this script in the same directory as the Pelican directory
- Update cdn_get_settings.py, update this line
  - sys.path.insert(0, "/path-to/pelican_cdn_sri")
  - This scripts require the script 'cdn_sri_module.py'from Pelican plugin pelican_cdn_sri
    Get the plugin from [here](https://github.com/patrickdung/pelican_cdn_sri)
- Create an INI file in the same directory as the Pelican directory, example:

```
[bootstrap]
cdn_type=cdnjs
version=5.1.1
css=css/bootstrap.min.css
js=js/bootstrap.min.js

[docs-searchbar.js]
cdn_type=jsdelivr
version=1.3.2
css=dist/cdn/docs-searchbar.min.css
js=dist/cdn/docs-searchbar.min.js
```

With reference to the above example, the user could specify:
{{ BOOTSTRAP_CSS }} to generate a code block for Bootstrap css.
So the format is {{ APPLICTION_NAME_CSS }} .
Note you need to replace '-' and '.' with '_' for the application name.
The generated code block is:

```
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/bootstrap/5.1.1/css/bootstrap.min.css" integrity="sha512-6KY5s6UI5J7SVYuZB4S/CZMyPylqyyNZco376NM2Z8Sb8OxEdp02e1jkKk/wZxIEmjQ6DRCEBhni+gpr9c4tvA==" crossorigin="anonymous" referrerpolicy="no-referrer">
```

So, the format for using the JS docs searchbar in the above example would be:
{{ DOCS_SEARCHBAR_JS_JS }}.
The first '_JS' is there because the application name is called docs-searchbar.js
The last '_JS' is specifying that we want to use the JavaScript code block.
If you want to use the CSS of the docs-searchbar.js, then it would be:
{{ DOCS_SEARCHBAR_JS_CSS }}.


- Next, run the script cdn_get_settings.py. A parameter config file (cdn_sri_pelicanconf.py) would be generated.
- Next, include the parameter file (cdn_sri_pelicanconf.py) in the Pelican config.
Example: add 'from cdn_sri_pelicanconf import *' to pelicanconf.py
- Finally, run Pelican to rebuild your static pages
