define(
    ['jquery', 'underscore', 'backbone', 'app', 'crel', 'h5f', 'text!templates/modals/admin/users.html', 'select2'],
    function ($, _, Backbone, app, crel, h5f, myTemplate) {
        'use strict';
        var exports = {
            Collection: Backbone.Collection.extend({
                baseUrl: 'api/v1/users',
                params: {},
                url: function () {
                    return this.baseUrl + '?' + $.param(this.params);
                }
            }),
            GroupCollection: Backbone.Collection.extend({
                baseUrl: 'api/v1/groups',
                filter: '',
                url: function () {
                    return this.baseUrl + this.filter;
                }
            }),
            View: Backbone.View.extend({
                initialize: function () {
                    this.template = myTemplate;
                    this.customerContext = app.user.toJSON().current_customer;
                    this.collection = new exports.Collection();
                    this.collection.params = {};
                    this.listenTo(this.collection, 'sync', this.render);
                    this.collection.fetch();

                    this.groupCollection = new exports.GroupCollection();
                    this.listenTo(this.groupCollection, 'sync', this.render);
                    this.groupCollection.fetch();

                    $.ajaxSetup({traditional: true});
                    return this;
                },
                events: {
                    'click button[name=toggleAcl]'      :   'toggleAclAccordion',
                    'click button[name=toggleDelete]'   :   'confirmDelete',
                    'change input[name=groupSelect]'    :   'toggle',
                    'change input[name=customerSelect]' :   'toggle',
                    'change select[name=groups]'        :   'retrieveGroups',
                    'change select[name=customers]'     :   'retrieveCustomers',
                    'click button[name=deleteUser]'     :   'deleteUser',
                    'click #cancelNewUser'              :   'displayAddUser',
                    'click #submitUser'                 :   'verifyForm',
                    'click #addUser'                    :   'displayAddUser',
                    'change #customerContext'           :   'changeCustomerContext',
                    'submit form'                       :   'submit'
                },
                retrieveGroups: function(event) {
                    this.groupsArray = event.val;
                    return this;
                },
                retrieveCustomers: function(event) {
                    this.customersArray = event.val;
                    return this;
                },
                changeCustomerContext: function (event) {
                    this.collection.params.customer_context = this.customerContext = event.val;
                    this.collection.fetch();
                    return this;
                },
                toggleAclAccordion: function (event) {
                    var $href = $(event.currentTarget),
                        $icon = $href.find('i'),
                        $accordionParent = $href.parents('.accordion-group'),
                        $accordionBody = $accordionParent.find('.accordion-body').first();
                    $icon.toggleClass('icon-circle-arrow-down icon-circle-arrow-up');
                    $accordionBody.unbind().collapse('toggle');
                    $accordionBody.on('hidden', function (event) {
                        event.stopPropagation();
                    });
                    return this;
                },
                displayAddUser: function (event) {
                    event.preventDefault();
                    var $addUserDiv = this.$('#newUserDiv');
                    $addUserDiv.toggle();
                    return this;
                },
                confirmDelete: function (event) {
                    var $parentDiv = $(event.currentTarget).parent();
                    $parentDiv.children().toggle();
                    return this;
                },
                deleteUser: function (event) {
                    var $deleteButton = $(event.currentTarget),
                        $userRow = $deleteButton.parents('.item'),
                        $alert = this.$el.find('div.alert'),
                        user = $deleteButton.val();
                    $.ajax({
                        type: 'DELETE',
                        url: '/api/v1/user/' + user,
                        dataType: 'json',
                        contentType: 'application/json',
                        success: function(response){
                            if (response.rv_status_code) {
                                $userRow.remove();
                                $alert.removeClass('alert-error').addClass('alert-success').show().find('span').html(response.message);
                            } else {
                                $alert.removeClass('alert-success').addClass('alert-error').show().find('span').html(response.message);
                            }
                        }
                    });
                    return this;
                },
                verifyForm: function (event) {
                    var form = document.getElementById('newUserDiv');
                    if (form.checkValidity()) {
                        this.submitNewUser(event);
                    }
                    return this;
                },
                submitNewUser: function (event) {
                    event.preventDefault();
                    var fullName = this.$el.find('#fullname').val(),
                        email = this.$el.find('#email').val(),
                        username = this.$el.find('#username').val(),
                        password = this.$el.find('#password').val(),
                        group = this.$el.find('select[name=groups]').select2('val'),
                        customers = this.$el.find('select[name=customers]').select2('data'),
                        $alert = this.$('#newUserDiv').find('.help-online'),
                        params = {
                            fullname: fullName,
                            email: email,
                            username: username,
                            password: password,
                            customer_context: this.customerContext
                        },
                        that = this;

                    params.group_ids = this.groupsArray;
                    params.customer_names = this.customersArray;

                    $.ajax({
                        type: 'POST',
                        url: '/api/v1/users',
                        data: JSON.stringify(params),
                        dataType: 'json',
                        contentType: 'application/json',
                        success: function(response) {
                            if (response.rv_status_code) {
                                that.collection.fetch();
                            } else {
                                $alert.removeClass('alert-success').addClass('alert-error').html(response.message).show();
                            }
                        }
                    }).error(function (e) { window.console.log(e.statusText); });
                    return this;
                },
                toggle: function (event) {
                    var $input = $(event.currentTarget),
                        username = $input.data('user'),
                        groupId = $input.data('id'),
                        url =  'api/v1/user/' + username,
                        $alert = this.$el.find('div.alert'),
                        params,
                        users = [],
                        groups = [];
                    users.push(username);
                    groups.push(groupId);
                    params = {
                        group_ids: groups,//event.added ? event.added.text : event.removed.text,
                        action: event.added ? 'add' : 'delete'
                    };
                    $.ajax({
                        type: 'POST',
                        url: url + '?' + $.param(params),
                        data: JSON.stringify(params),
                        dataType: 'json',
                        contentType: 'application/json',
                        success: function(response) {
                            if (response.rv_status_code) {
                                $alert.hide();
                            } else {
                                $alert.removeClass('alert-success').addClass('alert-error').show().find('span').html(response.message);
                            }
                        }
                    }).error(function (e) { window.console.log(e.responseText); });
                    return this;
                },
                beforeRender: $.noop,
                onRender: function () {
                    var $groups = this.$('select[name=groups]'),
                        $customers = this.$('select[name=customers]'),
                        $select = this.$el.find('input[name=groupSelect], input[name=customerSelect]'),
                        that = this;
                    $groups.select2({width: '100%'});
                    $customers.select2({width: '100%'});
                    _.each($select, function(select) {
                        if($(select).data('user') === 'admin')
                        {
                            $(select).select2({
                                width: '100%',
                                multiple: true,
                                initSelection: function (element, callback) {
                                    var data = JSON.parse(element.val()),
                                        results = [];
                                    _.each(data, function (object) {
                                        results.push({locked: true, id: object.group_id || object.customer_name, text: object.group_name ? object.group_name : object.customer_name});
                                    });
                                    callback(results);
                                },
                                ajax: {
                                    url: function () {
                                        return $(select).data('url');
                                    },
                                    data: function () {
                                        return {
                                            customer_name: that.customerContext
                                        };
                                    },
                                    results: function (data) {
                                        var results = [];
                                        if (data.rv_status_code === 1001) {
                                            _.each(data.data, function (object) {
                                                results.push({id: object.group_id || object.customer_name, text: object.group_name ? object.group_name : object.customer_name});
                                            });
                                            return {results: results, more: false, context: results};
                                        }
                                    }
                                }
                            });
                        }
                        else
                        {
                            $(select).select2({
                                width: '100%',
                                multiple: true,
                                initSelection: function (element, callback) {
                                    var data = JSON.parse(element.val()),
                                        results = [];
                                    _.each(data, function (object) {
                                        results.push({id: object.group_id || object.customer_name, text: object.group_name ? object.group_name : object.customer_name});
                                    });
                                    callback(results);
                                },
                                ajax: {
                                    url: function () {
                                        return $(select).data('url');
                                    },
                                    data: function () {
                                        return {
                                            customer_name: that.customerContext
                                        };
                                    },
                                    results: function (data) {
                                        var results = [];
                                        if (data.rv_status_code === 1001) {
                                            _.each(data.data, function (object) {
                                                results.push({id: object.group_id || object.customer_name, text: object.group_name ? object.group_name : object.customer_name});
                                            });
                                            return {results: results, more: false, context: results};
                                        }
                                    }
                                }
                            });
                        }
                    });
                    return this;
                },
                render: function () {
                    if (this.beforeRender !== $.noop) { this.beforeRender(); }

                    var template = _.template(this.template),
                        data = this.collection.toJSON()[0],
                        groups = this.groupCollection.toJSON()[0],
                        customers = app.user.toJSON(),
                        payload;
                    if (data && data.rv_status_code === 1001 && groups && groups.rv_status_code === 1001) {
                        payload = {
                            data: data.data,
                            groups: groups.data,
                            customers: customers.customers,
                            currentCustomer: this.customerContext,
                            viewHelpers: {
                                getOptions: function (options, selected) {
                                    var select = crel('select'), attributes;
                                    selected = selected || false;
                                    if (options.length) {
                                        _.each(options, function (option) {
                                            if (_.isUndefined(option.administrator) || option.administrator) {
                                                if(option.group_name)
                                                {
                                                    attributes = {value: option.id};
                                                    if (selected && option.group_name === selected) {attributes.selected = selected;}
                                                    select.appendChild(crel('option', attributes, option.group_name));
                                                }
                                                else if(option.customer_name)
                                                {
                                                    attributes = {value: option.id || option.customer_name};
                                                    if (selected && option.customer_name === selected) {attributes.selected = selected;}
                                                    select.appendChild(crel('option', attributes, option.customer_name));
                                                }
                                            }
                                        });
                                    }
                                    return select.innerHTML;
                                },
                                renderDeleteButton: function (user) {
                                    var fragment;
                                    if (user.user_name !== 'admin') {
                                        fragment = crel('div');
                                        fragment.appendChild(
                                            crel('button', {class: 'btn btn-link noPadding', name: 'toggleDelete'},
                                                crel('i', {class: 'icon-remove', style: 'color: red'}))
                                        );
                                        return fragment.innerHTML;
                                    }
                                },
                                renderUserLink: function (user) {
                                    var fragment = crel('div');
                                    fragment.appendChild(
                                        crel('button', {name: 'toggleAcl', class: 'btn btn-link noPadding'},
                                            crel('i', {class: 'icon-circle-arrow-down'}, ' '),
                                            crel('span', user.user_name)
                                        )
                                    );
                                    /*if (user.user_name !== 'admin') {
                                     fragment.appendChild(
                                     crel('button', {name: 'toggleAcl', class: 'btn btn-link noPadding'},
                                     crel('i', {class: 'icon-circle-arrow-down'}, ' '),
                                     crel('span', user.user_name)
                                     )
                                     );
                                     } else {
                                     fragment.appendChild(
                                     crel('strong', user.user_name)
                                     );
                                     }*/
                                    return fragment.innerHTML;
                                }
                            }
                        };
                        this.$el.empty();
                        this.$el.html(template(payload));

                        if (this.onRender !== $.noop) { this.onRender(); }
                    }
                    return this;
                }
            })
        };
        return exports;
    }
);
