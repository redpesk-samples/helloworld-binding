/*
 * Copyright (C) 2016 - 2020 "IoT.bzh"
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
#define _GNU_SOURCE
#include <stdio.h>
#include <string.h>
#include <json-c/json.h>
#include "wrap-json.h"

#define AFB_BINDING_VERSION 3
#include <afb/afb-binding.h>

static void pingSample(afb_req_t request)
{
	static int pingcount = 0;

	afb_req_success_f(request, json_object_new_int(pingcount), "Ping count = %d", pingcount);

	AFB_API_NOTICE(afbBindingV3root, "Verbosity macro at level notice invoked at ping invocation count = %d", pingcount);

	pingcount++;
}

// testArgsSample - return success only if argument is set to {"cezam": "open"}
static void testArgsSample(afb_req_t request)
{
	json_object *tmpJ;
	json_object *res = json_object_new_object();
	json_object *queryJ = afb_req_json(request);

	json_bool success = json_object_object_get_ex(queryJ, "cezam", &tmpJ);
	if (!success) {
		afb_req_fail_f(request, "ERROR", "key cezam not found in '%s'", json_object_get_string(queryJ));
		return;
	}

	if (json_object_get_type(tmpJ) != json_type_string) {
		afb_req_fail(request, "ERROR", "key cezam not a string");
		return;
	}

	if (strncmp(json_object_get_string(tmpJ), "open", 4) == 0) {
		json_object_object_add(res, "code", json_object_new_int(123456789));
		afb_req_success(request, res, NULL);
		return;
	}

	afb_req_fail_f(request, "ERROR", "value of cezam (%s) is not the expected one.",
				   json_object_get_string(queryJ));
}

static void infoSample(afb_req_t request) {

	json_object *response,
				*metadata, *groups,
				*generalgroup, *generalverbs,
				*infogroup, *infoverbs,
				*pingverb, *pingusage,
				*argsverb, *argsusage, *argssample,
				*rightargsample, *wrongargsample, *wrongargsampletwo,
				*infoverb;


	// Defining verbs
	wrap_json_pack(&pingusage, "{so*}",
                            "data", NULL
                        );
	wrap_json_pack(&pingverb, "{ss* ss* ss* so*}",
                            "uid", "ping",
                            "info", "sends ping",
							"api", "ping",
							"usage", pingusage
                        );

	wrap_json_pack(&argsusage, "{so*}",
                            "data", NULL
                        );

	wrap_json_pack(&rightargsample, "{ss*}",
                            "cezam", "open"
                        );
	wrap_json_pack(&wrongargsample, "{ss*}",
                            "foo", "bar"
                	);
	wrap_json_pack(&wrongargsampletwo, "{ss*}",
                            "cezam", "tada"
                	);
	argssample = json_object_new_array();
	json_object_array_add(argssample, wrongargsample);
	json_object_array_add(argssample, wrongargsampletwo);
	json_object_array_add(argssample, rightargsample);

	wrap_json_pack(&argsverb, "{ss* ss* ss* so* sO}",
                            "uid", "testargs",
                            "info", "Test arguments",
							"api", "testargs",
							"usage", argsusage,
							"sample", argssample
                        );

	wrap_json_pack(&infoverb, "{ss* ss* ss*}",
                            "uid", "info",
                            "info", "provides informations on this binding",
							"api", "info"
                        );

	// Defining groups of verbs
	groups = json_object_new_array();
	
	generalverbs = json_object_new_array();
	json_object_array_add(generalverbs, pingverb);
	json_object_array_add(generalverbs, argsverb);
	wrap_json_pack(&generalgroup, "{ss ss sO}",
                            "uid", "general",
                            "info", "verbs related to general tests on this binding",
                            "verbs", generalverbs
                        );	
	json_object_array_add(groups, generalgroup);

	infoverbs = json_object_new_array();
	json_object_array_add(infoverbs, infoverb);
	wrap_json_pack(&infogroup, "{ss ss sO}",
                            "uid", "info",
                            "info", "info verbs on this binding",
                            "verbs", infoverbs
                        );
	
	json_object_array_add(groups, infogroup);

	// Populating metadata for info verb
	wrap_json_pack(&metadata, "{ss* ss* ss*}", 
                            "uid", "Helloworld",
                            "info", "A simple Helloworld binding",
                            "version", "1.0"
                        );

	// Generate global response
	wrap_json_pack(&response, "{so, sO}","metadata", metadata, "groups", groups);
	afb_req_success(request, response, NULL);
}

static const struct afb_auth _afb_auths_v2_monitor[] = {
	{.type = afb_auth_Permission, .text = "urn:AGL:permission:monitor:public:set"},
	{.type = afb_auth_Permission, .text = "urn:AGL:permission:monitor:public:get"},
	{.type = afb_auth_Or, .first = &_afb_auths_v2_monitor[1], .next = &_afb_auths_v2_monitor[0]}
};

static const afb_verb_t verbs[] = {
	/*Without security*/
	{.verb = "ping", .session = AFB_SESSION_NONE, .callback = pingSample, .auth = NULL},

	/*With security "urn:AGL:permission:monitor:public:get"*/
	/*{ .verb = "ping"     , .session = AFB_SESSION_NONE, .callback = pingSample  , .auth = &_afb_auths_v2_monitor[1]},*/

	{.verb = "testargs", .session = AFB_SESSION_NONE, .callback = testArgsSample, .auth = NULL},
	{.verb = "info", .session = AFB_SESSION_NONE, .callback = infoSample, .auth = NULL},
	{NULL}
};

const afb_binding_t afbBindingExport = {
	.api = "helloworld",
	.specification = NULL,
	.verbs = verbs,
	.preinit = NULL,
	.init = NULL,
	.onevent = NULL,
	.userdata = NULL,
	.provide_class = NULL,
	.require_class = NULL,
	.require_api = NULL,
	.noconcurrency = 0
};
