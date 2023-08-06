# Adjutant

A basic workflow framework built using Django and Django-Rest-Framework to help automate basic Admin tasks within an OpenStack cluster.

Primarily built as user registration service that fits into the OpenStack ecosystem alongside Keystone, its purpose to fill functionality missing from Keystone. Ultimately it is just a framework with actions that are tied to an endpoint and can require certain data fields and perform actions via the OpenStack clients as well as talk to external systems as needed.

Useful for automating generic admin tasks that users might request but otherwise can't do without the admin role. Also allows automating the signup and creation of new users, but also allows such requests to require approval first if wanted. Due to issuing of uri+tokens for final steps of some actions, allows for a password submit/reset system as well.

### Functionality:

The main workflow consists of three possible steps which can be executed at different points in time, depending on how the TaskView is defined.

The base use case is three stages:

* Recieve Request
    * Validate request data against action serializers.
    * If valid, setup Task to represent the request, and the Actions specified for that TaskView.
    * The service runs the pre_approve function on all actions which should do any self validation to mark the actions themselves as valid or invalid, and populating the nodes in the Task based on that.
* Admin Approval
    * An admin looks at the Task and its notes.
    * If they decide it is safe to approve, they do so.
        * If there are any invalid actions approval will do nothing until the action data is updated and initial validation is rerun.
    * The service runs the post_approve function on all actions.
    * If any of the actions require a Token to be issued and emailed for additional data such as a user password, then that will occur.
        * If no Token is required, the Task will run submit actions, and be marked as complete.
* Token Submit
    * User submits the Token data.
    * The service runs the submit function on all actions, passing along the Token data, normally a password.
        * The action will then complete with the given final data.
    * Task is marked as complete.

There are cases and TaskViews that auto-approve, and thus automatically do the middle step right after the first. There are also others which do not need a Token and thus run the submit step as part of the second, or even all three at once. The exact number of 'steps' and the time between them depends on the definition of the TaskView.

Actions themselves can also effectively do anything within the scope of those three stages, and there is even the ability to chain multiple actions together, and pass data along to other actions.

The points that are modular, or will be made more modular in future, are the TaskViews and the actions tied to them. Adding new actions is easy, and attaching them to existing TaskViews is as well. Adding new TaskViews is also almost entirely modular.

Creation and management of Tasks, Tokens, and Notifications is not modular and is the framework around the defined Actions and TaskViews that handles how they are executed. This helps keep the way Actions are executed consistent and simpler to maintain, but does also allow Actions to run almost any logic within those consistent steps.

#### Admin Endpoints:

Endpoints for the management of tasks, tokens, and notifications. Most of these are limited by roles, or are for admin use only.

* ../v1/tasks - GET
    * A json containing all tasks.
        * Possible parameters are:
        * filters (specified below)
        * tasks_per_page, defaults to 25
        * page, page number to access (starts at 1)
* ../v1/tasks/<uuid> - GET
    * Get details for a specific task.
* ../v1/tasks/<uuid> - PUT
    * Update a task and retrigger pre_approve.
* ../v1/tasks/<uuid> - POST
    * approve a task
* ../v1/token - GET
    * A json containing all tokens.
        * Can also be filtered.
* ../v1/token - POST
    * Reissue tokens for a given task.
* ../v1/token - DELETE
    * Delete all expired tokens.
* ../v1/token/<uuid> - GET
    * return a json describing the actions and required fields for the token.
* ../v1/token/<uuid> - POST
    * submit the token.
* ../v1/notification - GET
    * Get a list of all unacknowledged notifications.
        * Can also be filtered.
* ../v1/notification - POST
    * Acknowledge a list of notifications.
* ../v1/notification/<id> - GET
    * Details on a specific notification.
* ../v1/notification/<id> - POST
    * Acknowledge a specific notification.

##### Filtering Tasks, Tokens, and Notifications

The task, token, and notification list endpoints can be filtered using a slight variant of the Django ORM filters.

This is done but sending a json with filters via HTTP parameters:
```javascript
{'filters': {'fieldname': { 'operation': 'value'}}
```

Example:
```javascript
{'filters': {'task_id': { 'exact': '842433bb-fa08-4fc1-8c3b-aa9904ceb370'}}
```

This looks a bit messy in the url as that json ends up being url-safe encoded, but doing the filters this way gives us a fairly large amount of flexibility.

Possible field lookup operations:
https://docs.djangoproject.com/en/1.8/ref/models/querysets/#id4


#### OpenStack Style TaskView Endpoints:

For ease of integration with OpenStack, these endpoints are setup to work and partly mimic the way similar ones would work in Keystone. They work and use the TaskViews, with some specical changes for certain required endpoints.

* ../v1/openstack/users - GET
    * Returns a list of users on your project, and their roles.
    * Also returns a list of pending user invites.
* ../v1/openstack/users - POST
    * authenticated endpoint limited by role
    * auto-approved
    * add/invite a user to your project
    * adds an existing user with the selected role, or if non-existent user sends a uri+token to them for setup user before adding the role.
    * allows adding of users to own project without needing an admin role
* ../v1/openstack/users/<user_id> - GET
    * Get details on the given user, including their roles on your project.
* ../v1/openstack/users/<user_id> - DELETE
    * Used to cancel a pending user invite.
* ../v1/openstack/users/<user_id>/roles - GET
    * Returns a list of roles for the user on your project.
* ../v1/openstack/users/<user_id>/roles - PUT
    * Add roles to a user.
* ../v1/openstack/users/<user_id>/roles - DELETE
    * Remove roles from a user.
* ../v1/openstack/roles - GET
    * Returns a list of roles you are allowed to edit on your project.
* ../v1/openstack/forgotpassword - POST
    * Submit a username/email to have a password reset token emailed to it.
* ../v1/openstack/email-update - POST
    * Submit a new email address for your user.
    * Will notifiy old email address, and send a uri+token to new email to confirm.
    * On confirm will update email (or username if username is email)
* ../v1/openstack/sign-up - POST
    * unauthenticated endpoint
    * for signup of new users/projects.
    * task requires manual approval, sends a uri+token for password setup after the project is created and setup.
        * create project
        * setup basic networking if needed
        * create user with random password
        * set user given password on token submit


#### (DEPRECATED) Default TaskView Endpoints:

Basic default endpoints for the TaskViews. These are still mostly used for testing, but are not really for production use. We will be getting rid of them eventually, although they do currently serve as a good basis for some of the more complex views.

* ../v1/actions/CreateProject - GET
    * return a json describing the actions and required fields for the endpoint.
* ../v1/actions/CreateProject - POST
    * unauthenticated endpoint
    * for signup of new users/projects.
    * task requires manual approval, sends a uri+token for password setup after the project is created and setup.
        * create project
        * setup basic networking if needed
        * create user with random password
        * set user given password on token submit
* ../v1/actions/InviteUser - GET
    * return a json describing the actions and required fields for the endpoint.
* ../v1/actions/InviteUser - POST
    * authenticated endpoint limited by role
    * auto-approved
    * add/invite a user to your project
    * adds an existing user with the selected role, or if non-existent user sends a uri+token to them for setup user before adding the role.
    * allows adding of users to own project without needing an admin role
* ../v1/actions/EditUser - GET
    * return a json describing the actions and required fields for the endpoint.
    * also returns a list of users that can be edited on your project.
* ../v1/actions/EditUser - POST
    * authenticated endpoint limited by role
    * auto-approved
    * add/remove roles from a user on your project
* ../v1/actions/ResetPassword - GET
    * return a json describing the actions and required fields for the endpoint.
* ../v1/actions/ResetPassword - POST
    * unauthenticated endpoint
    * auto-approved
    * issue a uri+token to user email to reset password
* ../v1/actions/UpdateEmail - GET
    * return a json describing the actions and required fields for the endpoint.
* ../v1/actions/UpdateEmail - POST
    * Authenticated but open to any user
    * auto-approved
    * takes an email address
    * issue a uri+token to new email to update to that email

#### More API Documentation:

While in debug mode the service will supply online browsable documentation via Django REST Swagger.

This is viewable at:
* ../docs

### Implementation Details:

#### Project Requirements:

The requirements for the service started as a system capable of taking requests for user sign up, waiting for approval, then on approval doing various setup and creation actions, followed by sending a uri+token to the user to set their password.

Creating a user directly in Keystone before approval also was to be avoided, and storing the password before approval was to be avoided.

Due to the steps involved, and the time between them, data had to be stored somewhere, and some representation of the request had to be stored as well. The ability to tie other actions and pieces of automation to the process also seemed useful and time saving considering the steps setting up a user might involve.

If that was the case, the system should ideally also have been modular enough to allow swapping of actions if circumstances changed, or new pieces of automation needed to be added or removed. Pushing as much logic to the concept of an 'action' seemed the ideal situation.

#### What is an Action?

Actions are a generic database model which knows what 'type' of action it is. On pulling the actions related to a Task from the database we wrap it into the appropriate class type which handles all the logic associated with that action type.

An Action is both a simple database representation of itself, and a more complex in memory class that handles all the logic around it.

Each action class has the functions "pre_approve", "post_approve", and "submit". These relate to stages of the approval process, and any python code can be executed in those functions, some of which should ideally be validation that the data passed makes sense.

Multiple actions can be chained together under one Task and will execute in the defined order. Actions can pass information along via an in memory cache/field on the task object, but that is only safe for the same stage of execution. Actions can also store data back to the database if their logic requires some info passed along to a later step of execution.

See **actions.models** and **actions.v1** for a good idea of Actions.

#### What is a Task?

A task is a top level model representation of the request. It wraps the request metadata, and based on the TaskView, will have actions associated with it.

See **api.models**.

#### What is a Token?

A token is a unique identifier linking to a task, so that anyone submitting the token will submit to the actions related to the task.

See **api.models**.

#### What is an TaskView

TaskViews are classes which extend the base TaskView class and use its imbuilt functions to process actions. They also have actions associated with them and the inbuilt functions from the base class are there to process and validate those against data coming in.

The TaskView will process incoming data and build it into a Task, and the related Action classes.

They are very simple to define as the inbuilt functions handle all the real logic, but defining which functions of those are called changes the view to create a task that either requires approval or auto-approves, with some cases auto-approval coming from the actions themselves if setup to do so.

The base TaskView class has three functions:

* get
    * just a basic view function that by default returns list of actions, and their required fields for the action view.
* process_actions
    * needs to be called in the TaskView definition
    * A function to run the processing and validation of request data for actions.
    * Builds and returns the task object, or the validation errors.
* approve
    * Takes a task and approves it, running post_approve actions and issuing a token if needed.
    * Used only if no admin approval is needed for Tasks create by this TaskView.

See **api.v1.tasks** and look at the TaskView class to get a better idea.

For a more complex variant, look at **api.v1.openstack** to see some more unique TaskViews specific to certain endpoints we needed to mimic OpenStack functionality.

In fact, at base these are ApiViews from Django Rest Framework, with some magic built in functions for task processing. You normally will want to pick a HTTP method for your core task itself, but having the other methods return data related to the task, or even trigger slight variants of a task is doable.


## Development:

### Packaging and Installing:

While this is a Django application, it does not follow the standard Django folder structure because of certain packaging requirements. As such the project does not have a manage.py file and must be installed via setup.py or pip (if an sdist is built) to access the manage.py funcationality.

Rather than a standard Django application, treat this as a more standard python application in this regard.

Once installed, all the normal manage.py functions can be called directly on the 'adjutant-api' commandline function.

### Dev Environment:

Dev is mainly done within a virtualenv setup alongside a devstack deployment.

For more info, see:
```
DEVSTACK_GUIDE.md
```

### Running tests:

We use tox to build a venv and run the tests. The same tests are also run for us in CI via jenkins.

Provided you have tox and its requirements installed running tests is very simple:

```
$ tox
```
To run just action unit tests:
```
$ tox -- adjutant.actions
```
To run a single api test:
```
$ tox -- adjutant.api.v1.tests.test_api_taskview.TaskViewTests.test_duplicate_tasks_new_user
```

### Adding Actions:

Adding new actions is done by creating a new django app in the actions module and defining the action models and their serializers. Action must extend the BaseAction class as defined in the **actions.models.v1.base** module. They also must register themselves to the global store of actions in **action.models**.

The documentation for this is mainly inline.

For examples of actions look in: **action.models.v1.users**, **action.models.v1.project**, and **action.models.v1.resources**

### Adding TaskViews:

TaskViews also need to be registered, and then are made active in the conf. To see how to register a TaskView look at **api.v1.models** and in the default conf under **ACTIVE_TASKVIEWS** too see how they are enabled.

For examples see **api.v1.openstack**.


## Setup/Deployment:

### Custom Email Templates

Custom email templates are placed in:
```
/etc/adjutant/templates/
```
This is so that adding personalised or deployment specific templates is kept outside of the scope of the service itself and managed by the deployer.

## Plugins

As Adjutant is built on top of Django, we've used parts of Django's installed apps system to allow us a plugin mechanism that allows additional actions and views to be brought in via external sources. This allows company specific or deployer specific changes to easily live outside of the core service and simply extend the core service where and when need.

An example of such a plugin is here:
https://github.com/catalyst/adjutant-odoo

## Future Plans:

Most future plans are around adding additional Actions to the service, but there will be some features that will require some refactoring.

While we are presently working with the Keystone V3 API, groups are not being used, but we intend to update the service to also manage and handle user groups. Managing Domains isn't really doable, but having the service be able to accept Domains, and multiple Domain back-ends is being planned.

Additional Actions and TaskViews we wish to add in the near future:

* Update Quota
    * Admin is required to do this
    * Allows users to request a quota increase and by requiring an admin to simply check, and confirm the request, will make the process faster.
    * Makes it effectively a quick 2 step process.
    * For eventual heirarchical-multi-tenancy this would ideally send these qouta increase requests to the parent for approval.
* Hierarchical Multi-Tenancy in a single domain environment
     * 'project_admin' to be able to create sub-projects off the current scoped project.
     * This works as per normal in Keystone but does not require an admin role and enforces a naming convention to ensure unique namespaces per sub-projects and somewhat avoid the project name uniqueness issues per domain.
     * This also adds inherited role support to the already existing user invite and user role editing features.
     * some VERY basic sub-project quota (number of sub-projects allowed) via metadata stored on a project in Keystone, with quota calculations in Adjutant checking against number of sub-projects created in your WHOLE tree within given shifting window.
* Stand-alone Setup Network Action + TaskView
    * For users who missed or forgot the step at Project creation, and want a quick network setup.
* Blank Slate
    * Doesn't need admin, and could reuse your own token.
    * Clear my entire project of any and all resources.
    * Already doable via the APIs, but would be nice to have it in an easy to request action so clients don't need to code it themselves.
* A way to setup and manage MFA credentials for a user
    * relies on work in Keystone around MFA, and serves only as a means to allow an initial challenge response that requires an initial passcode before MFA would become active for the user in Keystone.

Features that might require a slight refactor:

* Add optional serializers for token data.

Even less likely, and further far-future additions:

* Split the system into the api, a queue, and workers. That way tasks are processed asynchronously by the workers.
    * Will require a bunch of rethinking, but most of the core logic will be reused, with the workers simply waiting for events and executing them on the tasks/actions in much the same way as they are presently.
* Remove concept of predefined action steps entirely, setup Actions to have any possible number of 'steps'.
    * Will require moving actions to an iterator style pattern with a "next_action" style function as the driving force.
    * Will alter how chaining actions together works, thus may require a lot of work to define a sensible pattern for chaining them together.
