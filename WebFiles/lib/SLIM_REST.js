angular.module('SLIMResourceHttp', ['ngResource'])

    .factory('$SLIMResourceHttp', [ '$http', function ($http) {

        function SLIMResourceFactory(collectionName) {

            var config = angular.extend({ BASE_URL: 'db/' })
            var dbUrl = config.BASE_URL
            var collectionUrl = dbUrl + collectionName
            var resourceRespTransform = function (data) {
                return new Resource(data)
            }

            var resourcesArrayRespTransform = function (data) {
                var result = []
                for (var i = 0; i < data.length; i++) {
                    result.push(new Resource(data[i]))
                }
                return result
            }

            var promiseThen = function (httpPromise, successcb, errorcb, fransformFn) {
                return httpPromise.then(function (response) {
                    var result = fransformFn(response.data);
                    (successcb || angular.noop)(result, response.status, response.headers, response.config)
                    //alert('response: ' + JSON.stringify(response))
                    return result
                }, function (response) {
                    (errorcb || angular.noop)(undefined, response.status, response.headers, response.config)
                    //alert('error_promise: ' + JSON.stringify(response)+errorcb)
                    return undefined
                })
            }

            var preparyQueryParam = function (queryJson) {
                return angular.isObject(queryJson) && !angular.equals(queryJson, {}) ? {q: JSON.stringify(queryJson)} : {}
            }

            var Resource = function (data) {
                angular.extend(this, data)
            }

            Resource.query = function (queryJson, options, successcb, errorcb) {
                var RecordsLimit = ''
                if (queryJson != undefined) {
                    RecordsLimit = queryJson
                }
                //RecordsLimit --> " / START-AT / NUM-RECORDS "
                var httpPromise = $http.get(collectionUrl + RecordsLimit)
                return promiseThen(httpPromise, successcb, errorcb, resourcesArrayRespTransform)
            }

            Resource.queryPX = function (queryJson, options, successcb, errorcb) {
                var prepareOptions = function (options) {
                    var optionsMapping = {sort: 's', limit: 'l', fields: 'f', skip: 'sk'}
                    var optionsTranslated = {}
                    if (options && !angular.equals(options, {})) {
                        angular.forEach(optionsMapping, function (targetOption, sourceOption) {
                            if (angular.isDefined(options[sourceOption])) {
                                if (angular.isObject(options[sourceOption])) {
                                    optionsTranslated[targetOption] = JSON.stringify(options[sourceOption]);
                                } else {
                                    optionsTranslated[targetOption] = options[sourceOption];
                                }
                            }
                        })
                    }
                    return optionsTranslated
                }

                if (angular.isFunction(options)) {
                    errorcb = successcb;
                    successcb = options;
                    options = {}
                }

                var requestParams = angular.extend({}, preparyQueryParam(queryJson), prepareOptions(options))

                var httpPromise = $http.get(collectionUrl)

                return promiseThen(httpPromise, successcb, errorcb, resourcesArrayRespTransform)
            }

            Resource.all = function (options, successcb, errorcb) {
                if (angular.isFunction(options)) {
                    errorcb = successcb;
                    successcb = options;
                    options = {}
                }
                return Resource.query({}, options, successcb, errorcb);
            }

            Resource.count = function (queryJson, successcb, errorcb) {
                var httpPromise = $http.get(collectionUrl, {params: angular.extend({}, preparyQueryParam(queryJson), {c: true})})
                return promiseThen(httpPromise, successcb, errorcb, function (data) {
                    return data
                })
            }

            Resource.distinct = function (field, queryJson, successcb, errorcb) {
                var httpPromise = $http.post(dbUrl + '/runCommand', angular.extend({}, queryJson || {}, { distinct: collectionName, key: field}))
                return promiseThen(httpPromise, successcb, errorcb, function (data) {
                    return data.values
                })
            }

            Resource.getById = function (id, successcb, errorcb) {
                var httpPromise = $http.get(collectionUrl + '/' + id)
                return promiseThen(httpPromise, successcb, errorcb, resourceRespTransform)
            }

            Resource.getByObjectIds = function (ids, successcb, errorcb) {
                var qin = []
                angular.forEach(ids, function (id) {
                    qin.push({$oid: id})
                })
                return Resource.query({_id: {$in: qin}}, successcb, errorcb)
            }

            //instance methods

            Resource.prototype.$id = function () {
                return this.SEQ
            }

            Resource.prototype.$save = function (successcb, errorcb) {
                var httpPromise = $http.post(collectionUrl + "/X", this)
                return promiseThen(httpPromise, successcb, errorcb, resourceRespTransform)
            }

            Resource.prototype.$updatex = function (successcb, errorcb) {
                var httpPromise = $http.put(collectionUrl + "/" + this.$id(), angular.extend({}, this, {_id: undefined}))
                return promiseThen(httpPromise, successcb, errorcb, resourceRespTransform)
            }

            Resource.prototype.$update = function (successcb, errorcb) {
                var httpPromise = $http.put(collectionUrl + "/" + this.SEQ, angular.extend({}, this))
                    .success(function (data, status, headers, config) {
                        //alert('ok_data: ' + JSON.stringify(data))
                        //alert('ok_status: ' + JSON.stringify(status))
                        //alert('ok_headers: ' + JSON.stringify(headers))
                        //alert('ok_config: ' + JSON.stringify(config))
                        return promiseThen(httpPromise, successcb, errorcb, resourceRespTransform)
                    })
                    .error(function (data, status, headers, config) {
                        alert('error_data: ' + status + '-> ' + JSON.stringify(data))
                        //alert('error_status: ' + JSON.stringify(status))
                        //alert('error_headers: ' + JSON.stringify(headers))
                        //alert('error_config: ' + JSON.stringify(config))
                        return promiseThen(httpPromise, successcb, errorcb, resourceRespTransform)
                    })
            }


            var updateProject = function (project, updateData) {
                $http.put('/api/projects/' + project._id, updateData)
                    .success(function (data, status, headers, config) {
                        updateObjectInArray(dataService.data.projects.$$v, project, data)
                    }).error(function (data, status, headers, config) {
                    })
            }

            Resource.prototype.$remove = function (successcb, errorcb) {
                var httpPromise = $http['delete'](collectionUrl + "/" + this.$id())
                //alert(this.SEQ)
                return promiseThen(httpPromise, successcb, errorcb, resourceRespTransform)
            }

            Resource.prototype.$saveOrUpdate = function (savecb, errorcb) {
                if (this.$id() > 0) {
                    return this.$update(savecb, errorcb)
                } else {
                    return this.$save(savecb, errorcb)
                }
            }

            return Resource
        }

        return SLIMResourceFactory
    }])