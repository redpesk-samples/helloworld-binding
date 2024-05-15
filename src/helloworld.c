#include <stdio.h>
#include <string.h>
#include <stdint.h>
#include <stdbool.h>
#include <json-c/json.h>

#define AFB_BINDING_VERSION 4
#include <afb/afb-binding.h>

/*************
EVENT CREATION 
*************/

/**
 * An event which is to be pushed to its subscribers every time a verb is called
 */
static afb_event_t verb_called_ev;

/* This is called at some crucial steps during the lifecycle of the
 * binding. We are only interested in the "init" stage, where we declare
 * an event which will be used later on by the binding. */
static int mainctl(afb_api_t api, afb_ctlid_t ctlid, afb_ctlarg_t ctlarg, void *userdata)
{
    if (ctlid == afb_ctlid_Init)
        /* Return the same code as `afb_api_new_event` so that the
         * initialisation fails if the event cannot be created */
        return afb_api_new_event(api, "verb_called", &verb_called_ev);

    /* Return 0 for all the other stages, otherwise initialisation will fail */
    return 0;
}

/*****************
CONTEXT MANAGEMENT
 & EVENT SUB/PUSH
*****************/

/**
 * Context initialization
 */
static int context_init_cb(void *closure, void **value, void (**freecb)(void*), void **freeclo)
{
    // The context is a simple boolean: false if client has not been subscribed yet, true if he is.
    // Avoid casting by using an intermediary `flag` variable.
    bool *flag = malloc(sizeof(*flag));
    *value = flag;
    // Context cleanup is just freeing the boolean, so we can simply pass `free` as the callback
    *freecb = free;
    *freeclo = flag; // `freeclo` is the argument passed to `free`, here our boolean pointer

    // Init the context to `false` since the client isn't subscribed yet
    *flag = false;

    return 0;
}

/**
 * Checks if the client is subscribed to verb_called_ev; if not, subscribes it
 */
static void check_subscription(afb_req_t req)
{
    bool* context;

    // Get context for the client who emitted the request, if it doesn't exist yet create it
    if (afb_req_context(req, (void**)&context, context_init_cb, NULL) == 1)
        AFB_REQ_NOTICE(req, "context initialized for new client");

    // If the client isn't subscribed yet, do it
    if (!*context) {
        afb_req_subscribe(req, verb_called_ev);
        *context = true;
    }
}

/**
 * Pushes a verb_called event
 */
static void pub_verb_called_ev(afb_req_t req)
{
    const char *called_verb;
    afb_data_t ev_data;

    // As an argument to the event, we use the called verb's name
    called_verb = afb_req_get_called_verb(req);
    afb_create_data_copy(&ev_data, AFB_PREDEFINED_TYPE_STRINGZ, called_verb, strlen(called_verb) + 1);

    // Before pushing the event, make sure the client is subscribed
    check_subscription(req);
    afb_event_push(verb_called_ev, 1, &ev_data);
}

/****
VERBS
****/

// Receives a string, replies with another string
static void hello_verb(afb_req_t req, unsigned nparams, afb_data_t const *params)
{
    int rc;
    afb_data_t name, reply;
    const char *who = "world", *who_arg;
    char reply_str[100];

    // Publish an event that a verb has been called
    pub_verb_called_ev(req);

    // Read request parameter; if there is one and it is not null, replace `who` with its content
    rc = afb_req_param_convert(req, 0, AFB_PREDEFINED_TYPE_STRINGZ, &name);
    if (rc == 0) {
        who_arg = afb_data_ro_pointer(name);
        if (strcmp("null", who_arg) != 0)

            who = who_arg;
    }

    // Create reply string; use snprintf to avoid overflows caused by a long enough parameter
    rc = snprintf(reply_str, sizeof(reply_str), "Hello %s!", who);
    reply_str[sizeof(reply_str) - 1] = '\0';
    afb_create_data_copy(&reply, AFB_PREDEFINED_TYPE_STRINGZ, reply_str, (size_t)(rc + 1));

    afb_req_reply(req, 0, 1, &reply);
}

// Receives a JSON array of integers, replies with the result of their sum
static void sum_verb(afb_req_t req, unsigned nparams, afb_data_t const *params)
{
    int rc;
    int64_t sum;
    size_t items;
    afb_data_t afb_arg, reply;
    struct json_object *arg, *item;
    const char * const err_msg = "parameter should be a JSON array of integers";

    // Publish an event that a verb has been called
    pub_verb_called_ev(req);

    // Check that the request has an appropriate number of parameters
    if (nparams != 1)
        goto err;
    // Convert the parameter to a json_object (parsing and memory management are handled by AFB)
    rc = afb_req_param_convert(req, 0, AFB_PREDEFINED_TYPE_JSON_C, &afb_arg);
    if (rc < 0)
        goto err;
    arg = afb_data_ro_pointer(afb_arg);
    // Check the JSON structure of the parameter
    if (json_object_get_type(arg) != json_type_array)
        goto err;

    // Sum all the integers given in the parameter (which we made sure is a JSON array)
    sum = 0;
    items = json_object_array_length(arg);
    for (size_t i = 0; i < items; i++) {
        item = json_object_array_get_idx(arg, i);
        // If an item is not an integer, stop and fail
        if (json_object_get_type(item) != json_type_int)
            goto err;
        sum += json_object_get_int64(item);
    }

    // Reply
    afb_create_data_copy(&reply, AFB_PREDEFINED_TYPE_I64, &sum, sizeof(int64_t));
    afb_req_reply(req, 0, 1, &reply);
    return;

err:
    AFB_API_ERROR(afb_req_get_api(req), err_msg);
    afb_create_data_copy(&reply, AFB_PREDEFINED_TYPE_STRINGZ, err_msg, strlen(err_msg) + 1);
    afb_req_reply(req, -1, 1, &reply);
}

/************
BINDING SETUP
************/

// List all the verbs we want to expose
static const afb_verb_t verbs[] = {
    {.verb = "hello", .callback = hello_verb},
    {.verb = "sum", .callback = sum_verb},
    {.verb = NULL} // This has the same meaning as the '\0' at the end of a string
};

// Binding/API configuration should not be static because the binder must access it
const afb_binding_t afbBindingExport = {
    .api = "helloworld",
    .verbs = verbs,
    .mainctl = mainctl
};
