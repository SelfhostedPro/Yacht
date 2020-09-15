from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.session import make_transient

from .. import models, schemas
from ...utils import conv_ports2dict, conv_sysctls2dict

from datetime import datetime
import urllib.request
from urllib.parse import urlparse
import json
import yaml
import os

# Templates


def get_templates(db: Session):
    return db.query(models.Template).all()


def get_template(db: Session, url: str):
    return db.query(models.Template).filter(models.Template.url == url).first()


def get_template_by_id(db: Session, id: int):
    return db.query(models.Template).filter(models.Template.id == id).first()


def get_template_items(db: Session, template_id: int):
    return db.query(models.TemplateItem).filter(models.TemplateItem.template_id == template_id).all()


def delete_template(db: Session, template_id: int):
    _template = db.query(models.Template).filter(
        models.Template.id == template_id).first()
    db.delete(_template)
    db.commit()
    return _template


def add_template(db: Session, template: models.containers.Template):
    try:
        _template_path = urlparse(template.url).path
        ext = os.path.splitext(_template_path)[1]
        # Opens the JSON and iterate over the content.
        _template = models.containers.Template(
            title=template.title, url=template.url)
        with urllib.request.urlopen(template.url) as file:
            if ext in (".yml", '.yaml'):
                loaded_file = yaml.load(file, Loader=yaml.SafeLoader)
            elif ext in (".json"):
                loaded_file = json.load(file)
            else:
                print('Invalid filetype')
                raise
            for entry in loaded_file:

                ports = conv_ports2dict(entry.get('ports', []))
                sysctls = conv_sysctls2dict(entry.get('sysctls', []))

                # Optional use classmethod from_dict
                template_content = models.containers.TemplateItem(
                    type=int(entry['type']),
                    title=entry['title'],
                    platform=entry['platform'],
                    description=entry.get('description', ''),
                    name=entry.get('name', entry['title'].lower()),
                    logo=entry.get('logo', ''),  # default logo here!
                    image=entry.get('image', ''),
                    notes=entry.get('note', ''),
                    categories=entry.get('categories', ''),
                    restart_policy=entry.get('restart_policy'),
                    ports=ports,
                    volumes=entry.get('volumes', []),
                    env=entry.get('env', []),
                    sysctls=sysctls,
                    cap_add=entry.get('cap_add', [])
                )
                _template.items.append(template_content)
    except (OSError, TypeError, ValueError) as err:
        # Optional handle KeyError here too.
        print('data request failed', err)
        raise

    try:
        db.add(_template)
        db.commit()
    except IntegrityError as err:
        # TODO raises IntegrityError on duplicates (uniqueness)
        #       status
        db.rollback()
        pass

    return get_template(db=db, url=template.url)


def refresh_template(db: Session, template_id: id):
    template = db.query(models.Template).filter(
        models.Template.id == template_id).first()

    _template_path = urlparse(template.url).path
    ext = os.path.splitext(_template_path)[1]

    items = []
    try:
        with urllib.request.urlopen(template.url) as fp:
            if ext in (".yml", '.yaml'):
                loaded_file = yaml.load(fp, Loader=yaml.SafeLoader)
            elif ext in (".json"):
                loaded_file = json.load(fp)
            else:
                print('Invalid filetype')
                raise
            for entry in loaded_file:

                ports = conv_ports2dict(entry.get('ports', []))
                sysctls = conv_sysctls2dict(entry.get('sysctls', []))

                item = models.TemplateItem(
                    type=int(entry['type']),
                    title=entry['title'],
                    platform=entry['platform'],
                    description=entry.get('description', ''),
                    name=entry.get('name', entry['title'].lower()),
                    logo=entry.get('logo', ''),  # default logo here!
                    image=entry.get('image', ''),
                    notes=entry.get('note', ''),
                    categories=entry.get('categories', ''),
                    restart_policy=entry.get('restart_policy'),
                    ports=ports,
                    volumes=entry.get('volumes', []),
                    env=entry.get('env', []),
                    sysctls=sysctls,
                    cap_add=entry.get('cap_add', [])
                )
                items.append(item)
    except Exception as exc:
        print('Template update failed. ERR_001', exc)
        raise
    else:
        # db.delete(template)
        # make_transient(template)
        # db.commit()

        template.updated_at = datetime.utcnow()
        template.items = items

        try:
            # db.add(template)
            db.commit()
            print(f"Template \"{template.title}\" updated successfully.")
        except Exception as exc:
            db.rollback()
            print('Template update failed. ERR_002', exc)
            raise

    return template


def read_app_template(db, app_id):
    try:
        template_item = db.query(models.TemplateItem).filter(
            models.TemplateItem.id == app_id).first()
        return template_item
    except Exception as exc:
        print('App template not found')
        raise


def set_template_variables(db: Session, new_variables: models.TemplateVariables):
    try:
        template_vars = db.query(models.TemplateVariables).all()

        variables = []
        t_vars = new_variables

        for entry in t_vars:
            template_variables = models.TemplateVariables(
                variable=entry.variable,
                replacement=entry.replacement
            )
            variables.append(template_variables)

        db.query(models.TemplateVariables).delete()
        db.add_all(variables)
        db.commit()

        new_template_variables = db.query(models.TemplateVariables).all()

        return new_template_variables

    except IntegrityError as err:
        abort(400, {'error': 'Bad Request'})


def read_template_variables(db: Session):
    return db.query(models.TemplateVariables).all()
