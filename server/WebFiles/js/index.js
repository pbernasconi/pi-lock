'use strict';
angular.module('to.app', ['ui.compat', 'ui', 'SLIMResourceHttp', 'angular-table', 'timer', 'ui.bootstrap'])


    .config( ['$stateProvider', '$routeProvider', '$urlRouterProvider',
            function ($stateProvider, $routeProvider, $urlRouterProvider) {


                $urlRouterProvider
                    .when('/p?id', '/personas/:id')
                    .otherwise('/')


                $routeProvider
                    .when('/', {
                        template: '<p class="lead">Bienvenido a Totai Citrus RFID</p>' +
                                  '<p>Use the menu above to navigate</p><p></p>' + '<HR>'
                    })


                $stateProvider
                    .state('permisos', {
                        url: '/permisos',
                        templateUrl: 'permisos.html',
                        resolve: {Permisos: "Permisos"},
                        controller: ['$scope', 'Permisos', '$state', '$stateParams', '$rootScope', '$http',
                            function ($scope, Permisos, $state, $stateParams, $rootScope, $http) {
                                $scope.accesos = {'0': "OK", '1': "X-X-X", '2': "Blocked", '3': "PIN", '4': "Error PIN", '5': "ALARMA"}
                                $scope.Permisos = []
                                $scope.Permisos = Permisos.query()
                                $scope.selectedRow = {}
                                $scope.handleRowSelection = function (row) {
                                    $scope.selectedRow = row
                                    $state.transitionTo('permisos.detail')
                                }
                                $scope.isClean = function () {
                                    return angular.equals($scope.original, $scope.persona)
                                }
                                $scope.pages = $rootScope.pagination
                                $scope.$watch('pages.currentPage', function (newPage) {
                                    $scope.pages.watchPage = newPage - 1
                                    $scope.update()
                                })
                                $scope.update = function () {
                                    $scope.Permisos = Permisos.query('/' + $scope.pages.watchPage + '/' + $scope.pages.maxDisplayRecords, '',
                                        function (data) {
                                            _.each(data, function (post) {
                                                _.extend(post, {test: $scope.pages.results[post.permiso]})
                                            })
                                        }
                                    )
                                }
                            }]
                    })
                    .state('permisos.detail', {
                        templateUrl: "permisos.detail.html"
                    })
                    .state('entrada', {
                        url: '/entrada',
                        templateUrl: 'entradas.html',
                        resolve: {Entrada: "Entrada"},
                        controller: ['$scope', 'Entrada', '$state', '$stateParams', '$rootScope', '$http',
                            function ($scope, Entrada, $state, $stateParams, $rootScope, $http) {
                                $scope.Entrada = []
                                $scope.selectedRow = {}
                                $scope.handleRowSelection = function (row) {
                                    $scope.selectedRow = row
                                }
                                $scope.pages = $rootScope.pagination
                                $scope.$watch('pages.currentPage', function (newPage) {
                                    $scope.pages.watchPage = newPage - 1
                                    $scope.update()
                                })
                                $scope.update = function () {
                                    $scope.Entrada = Entrada.query('/' + $scope.pages.watchPage + '/' + $scope.pages.maxDisplayRecords, '',
                                        function (data) {
                                            _.each(data, function (post) {
                                                _.extend(post, {test: $scope.pages.results[post.permiso]})
                                            })
                                        }
                                    )
                                }
                            }]
                    })
                    .state('configura', {
                        url: '/configura',
                        templateUrl: 'puerta.html',
                        resolve: {Puerta: "Puerta"},
                        controller: ['$scope', 'Puerta', '$state', '$stateParams', '$rootScope', '$http',
                            function ($scope, Puerta, $state, $stateParams, $rootScope, $http) {
                                $scope.Puerta = Puerta.query()
                                $scope.puerta = {}
                                $scope.timerRunning = true
                                $scope.timerConsole = ''
                                $scope.timerType = 'Polling'
                                $scope.lockRoom = true
                                $scope.ReadOnly = true
                                $scope.EditMe = function () {
                                    $scope.timerRunning = false
                                    $scope.$broadcast('timer-stop')
                                    $scope.ReadOnly = false
                                    $scope.original = $scope.puerta
                                }
                                $scope.isClean = function () {
                                    return angular.equals($scope.original, $scope.puerta)
                                }
                                $scope.save = function (){
                                    $http.put('up/putPuerta', '[' + JSON.stringify($scope.puerta) + ']').
                                        success(function (data, status) {
                                            alert(data)
                                            $http({method: 'GET', url: 'db/getPuerta'}).
                                                success(function (data, status) {
                                                    $scope.puerta = data[0]
                                                    //alert(angular.equals($scope.original, $scope.puerta))
                                                })
                                            $http.put('up/RESTART_PI-LOCK', '[{"R_PI" : "RESTART"}]').
                                                success(function (data, status) {
                                                    alert(data)
                                                })
                                        })
                                }
                                $scope.RestartPI = function(){
                                    $scope.timerRunning = false
                                    $scope.$broadcast('timer-stop')
                                    $http.put('up/RESTART_PI-LOCK', '[{"R_PI" : "RESTART"}]').
                                        success(function (data, status) {
                                            alert(data)
                                        })
                                }
                                $scope.InstallGithub = function(){
                                    $scope.timerRunning = false
                                    $scope.$broadcast('timer-stop')
                                    $http.put('up/RESTART_PI-LOCK', '[{"R_PI" : "GitHub"}]').
                                        success(function (data, status) {
                                            alert(data)
                                        })
                                }
                                $scope.toggle = function () {
                                    if ($scope.timerRunning == true) {
                                        $scope.$broadcast('timer-start')
                                    }
                                    else {
                                        $scope.$broadcast('timer-stop')
                                    }
                                }
                                $scope.startTimer = function () {
                                    $scope.$broadcast('timer-start')
                                    $scope.timerRunning = true
                                }
                                $scope.stopTimer = function () {
                                    $scope.$broadcast('timer-stop')
                                    $scope.timerRunning = false
                                }
                                $scope.fetch = function () {
                                    $http({method: 'GET', url: 'db/getPuerta'}).
                                        success(function (data, status) {
                                            $scope.puerta = data[0]
                                        })
                                    $http({method: 'GET', url: 'db/getEntradaX'}).
                                        success(function (data, status) {
                                            $scope.puertaLastX = data
                                        })
                                }
                                $scope.$on('timer-tick', function (event, args) {
                                    $scope.fetch()
                                    //$scope.timerConsole += $scope.timerType + ': ' + event.name + ', timeoutId: ' + args.timeoutId + '\n'
                                })

                                $scope.shouldBeOpen = false
                                $scope.open = function () {
                                    $scope.shouldBeOpen = true;
                                }
                                $scope.close = function () {
                                    $scope.closeMsg = 'I was closed at: ' + new Date()
                                    $scope.shouldBeOpen = false
                                }
                                $scope.restart = function () {
                                    $scope.shouldBeOpen = false
                                    //$http({method: 'GET', url: 'db/restart'}).
                                    $http.put('up/putPuerta', '[' + JSON.stringify($scope.puerta) + ']').
                                        success(function (data, status) {
                                            alert(data)
                                        })
                                }
                                $scope.items = ['item1', 'item2']
                                $scope.opts = {
                                    backdropFade: true,
                                    dialogFade: true
                                }
                            }]
                    })
                
            }])



    .factory('Puerta', function ($SLIMResourceHttp) {
        return $SLIMResourceHttp('getPuerta')
    })
    .factory('Permisos', function ($SLIMResourceHttp) {
        return $SLIMResourceHttp('getPermisos')
    })
    .factory('Entrada', function ($SLIMResourceHttp) {
        return $SLIMResourceHttp('getEntrada')
    })



    .run([   '$rootScope', '$state', '$stateParams',
        function ($rootScope, $state, $stateParams) {
            $rootScope.$state = $state
            $rootScope.$stateParams = $stateParams

            $rootScope.pagination = []
            $rootScope.pagination.results = [ "OK", "X-X-X", "Blocked", "PIN", "Error PIN", "ALARMA"]
            $rootScope.pagination.list = [
                {id: 10, name: "10 items"},
                {id: 50, name: "50 items"},
                {id: 100, name: "100 items"},
                {id: 1000, name: "1000 items"}
            ]
            $rootScope.pagination.prevText = '<'
            $rootScope.pagination.nextText = '>'
            $rootScope.pagination.firstText = '<<'
            $rootScope.pagination.lastText = '>>'
            $rootScope.pagination.maxDisplayPages = 100
            $rootScope.pagination.maxDisplayRecords = 10
            $rootScope.pagination.currentPage = 1
            $rootScope.pagination.maxSize = 5
            $rootScope.pagination.watchPage = 0
        }])