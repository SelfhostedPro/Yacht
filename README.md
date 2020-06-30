## Yacht
Yacht is a flask based container management UI with a focus on templates and 1-click deployments.

## Demo:
![Tempaltes](readme_media/Yacht-Demo.gif "templates")

## Installation:
Currently only linux has been verified as working but we are open to the idea of supporting windows eventually as well.

**Keep in mind, this is an Alpha so the risk of data loss is real and it may not be stable**

Once docker is installed you'll simply run the following commands to get started:
```
docker volume create yacht
docker run -d -p 5000:5000 -v /var/run/docker.sock:/var/run/docker.sock -v yacht:/config selfhostedpro/yacht:latest
```
It will be available on port 5000.
The default username is `admin@yacht.local`.
The default password is `password`.
You can change these by setting the `ADMIN_EMAIL` and `ADMIN_PASSWORD` environment variables or in the account settings within the application.

## Features So Far:
* User Management
* User and Admin Roles
* Container Templating Compatibility (Portainer Compatible)
* Semantic UI Framework
* Basic Container Management
* Template Framework
* Easy Template Updating

## Planned Features:
* Advanced Container Management (Edit, Modify, Create without a template)
* Container Monitoring
* Docker-Compose Compatibility
* Easy access to container interfaces
* Centralized settings for volume management and similar QOL functionality.

*If you want something that's not planned please open a feature request issue and we'll see about getting it added.*

## Templating:
Currently Yacht is compatible with portainer templates. You'll add a template url in the "Add Template" settings. The the template will be read, separated into apps, and imported into the database. The apps associated with the templates are linked via a db relationship so when the template is removed, so are the apps associated with it. We store the template url as well so we can enable updating templates with a button press.

We recommend starting with: https://raw.githubusercontent.com/SelfhostedPro/selfhosted_templates/yacht/Template/template.json

## License
[MIT License](LICENSE.md)
