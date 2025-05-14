#include <json-c/json.h>
#include <cstring>

#define AFB_BINDING_VERSION 4
#include <afb/afb-binding>

/*************
EVENT CREATION
*************/

/**
 * An event which is to be pushed to its subscribers every time a verb is called
 */
static afb::event verb_called_ev;

/* This is called at some crucial steps during the lifecycle of the
 * binding. We are only interested in the "init" stage, where we declare
 * an event which will be used later on by the binding. */
static int mainctl(afb::api api,
                   afb::ctlid ctlid,
                   const afb::ctlarg ctlarg,
                   void *userdata) noexcept
{
    if (ctlid == afb_ctlid_Init) {
        // Return -1 if the initialized event is not valid, which will fail the initialization
        verb_called_ev = api.new_event("verb_called");
        if (!verb_called_ev.is_valid())
            return -1;
    }

    // Return 0 for all the other stages, otherwise initialisation will fail
    return 0;
}

/*****************
CONTEXT MANAGEMENT
 & EVENT SUB/PUSH
*****************/

/**
 * Checks if the client is subscribed to verb_called_ev; if not, subscribes it
 */
static void check_subscription(afb::req req)
{
    auto ctx(req.context<char>());

    if (!ctx) {
        AFB_REQ_NOTICE(req, "context initialized for new client");
        ctx.set(new char('z'));
        req.subscribe(verb_called_ev);
    }
}

/**
 * Pushes a verb_called event
 */
static void pub_verb_called_ev(afb::req req)
{
    const char *called_verb;

    // As an argument to the event, we use the called verb's name
    called_verb = afb_req_get_called_verb(req);
    afb::data ev_data(afb::STRINGZ(), called_verb, strlen(called_verb) + 1);

    // Before pushing the event, make sure the client is subscribed
    check_subscription(req);
    verb_called_ev.push(ev_data);
}

/****
VERBS
****/

// Receives a string, replies with another string
static void hello_verb(afb::req req, afb::received_data params)
{
    int rc;
    const char *who = "world";
    const char *who_arg;
    char reply_str[100];

    // Publish an event that a verb has been called
    pub_verb_called_ev(req);

    // Read request parameter; if there is one and it is convertable to a string, replace "who" with
    // its content
    if (req.try_convert(0, afb::STRINGZ())) {
        who_arg = (const char *)*(params[0]);
        if (strcmp("null", who_arg) != 0)
            who = who_arg;
    }

    // Create reply string; use snprintf to avoid overflows caused by a long enough parameter
    rc = snprintf(reply_str, sizeof(reply_str), "Hello %s!", who);
    reply_str[sizeof(reply_str) - 1] = '\0';

    // Create reply data and reply
    afb::data reply(afb::STRINGZ(), reply_str, (size_t)(rc + 1));
    req.reply(0, reply);
}

// Receives a JSON array of integers, replies with the result of their sum
static void sum_verb(afb::req req, afb::received_data params)
{
    int64_t sum;
    size_t items;
    struct json_object *arg, *item;

    // Publish an event that a verb has been called
    pub_verb_called_ev(req);

    // Check that the request has an appropriate number of parameters
    if (params.size() != 1)
        goto err;
    // Convert the parameter to a json_object (parsing and memory management are handled by AFB)
    if (req.try_convert(0, afb::JSON_C()))
        // try_convert replaces the old value by the converted one, so now we can use the parameter
        // directly
        arg = (json_object *)*(params[0]);
    else
        goto err;
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
    {  // Scope needed otherwise the compiler tells us that the `goto` statements bypass reply's
       // initialization
        afb::data reply(afb::I64(), &sum, sizeof(int64_t));
        req.reply(0, reply);
    }
    return;

err:
    const char *const err_msg = "parameter should be a JSON array of integers";
    AFB_API_ERROR(afb_req_get_api(req), err_msg);
    afb::data reply(afb::STRINGZ(), err_msg, strlen(err_msg) + 1);
    req.reply(-1, reply);
}

extern const char *info_verb_json;

static void info_verb(afb::req req, afb::received_data params)
{
    enum json_tokener_error jerr;

    json_object *info_obj = json_tokener_parse_verbose(info_verb_json, &jerr);
    if (info_obj == NULL || jerr != json_tokener_success) {
        const char *err_msg = "error parsing info() verb description";
        AFB_API_ERROR(afb_req_get_api(req), err_msg);
        afb::data reply(afb::STRINGZ(), err_msg, strlen(err_msg) + 1);
        req.reply(-1, reply);
        return;
    }

    afb::data reply(afb::JSON_C(), info_obj, 0, (void (*)(void *))json_object_put, info_obj);
    req.reply(0, reply);
    return;
}

/************
BINDING SETUP
************/

// List all the verbs we want to expose
static const afb_verb_t verbs[] = {
    afb::verb<info_verb>("info"), afb::verb<hello_verb>("hello"), afb::verb<sum_verb>("sum"),
    afb::verbend()  // This has the same meaning as the '\0' at the end of a string
};

// Binding/API configuration should not be static because the binder must access it
const afb_binding_t afbBindingExport = afb::binding<mainctl>("helloworld", verbs);
