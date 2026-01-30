from cement import Controller, ex, shell


def get_pool_members(conn, pool_id):
    memberdata = {}
    members = conn.load_balancer.members(pool_id)
    for member in members:
        memberdata[member.id] = {
            'project_id': member.project_id,
            'name': member.name,
            'provisioning_status': member.provisioning_status,
            'operating_status': member.operating_status,
            'dest': "{}:{}".format(member.address, member.protocol_port)
        }
    return memberdata


def get_listener_info(conn, listener_list):
    listenerdata = {}
    for listener in listener_list:
        listener_obj = conn.load_balancer.get_listener(listener['id'])
        members = get_pool_members(conn, listener_obj.default_pool_id)
        listenerdata[listener_obj.id] = {
            'port_proto': "{}{}".format(listener_obj.protocol_port,
                listener_obj.protocol),
            'pool_id': listener_obj.default_pool_id,
            'name': listener_obj.name,
            'project_id': listener_obj.project_id,
            'members': members
        }
    return listenerdata


def get_load_balancer_info(self, conn):

    lbs = conn.load_balancer.load_balancers()
    ips = list(conn.network.ips())

    lbdata = {}
    bad_lbs = {}
    for lb in lbs:
        # Correlate project IDs to project names
        try:
            project_name = conn.identity.get_project(lb.project_id)
        except self.app.err.NotFoundException:
            project_name = 'missing'

        # Correlate floating IP addresses and VIP addresses
        floating_ip_addr = 'none'
        for floating_ip in ips:
            if floating_ip.fixed_ip_address == lb.vip_address and \
                floating_ip.port_id == lb.vip_port_id:
                floating_ip_addr = floating_ip.floating_ip_address

        # Correlate listener data
        listenerdata = get_listener_info(self.app.conn, lb.listeners)

        # Select the broken ones and put all the data in a dict
        if project_name == 'missing' or lb.operating_status == 'ERROR':
            lbdata[lb.id] = {
                'id': lb.id,
                'data': {
                    'vip': lb.vip_address,
                    'project_id': lb.project_id,
                    'project_name': project_name,
                    'vip_address': lb.vip_address,
                    'floating_ip': floating_ip_addr,
                    'operating_status': lb.operating_status,
                    'provisioning_status': lb.provisioning_status,
                    'listeners': listenerdata
                }
            }

    return lbdata


def delete_load_balancer(self, conn, lb_id):
    # Deletes a loadbalancer
    self.app.log.info('Deleting: %s' % lb_id, __name__)
    res = conn.load_balancer.delete_load_balancer(lb_id, True, True)
    return res


class LoadBalancer(Controller):
    class Meta:
        label = "lb"
        stacked_type = 'embedded'
        stacked_on = 'base'
        output_handler = 'yaml'

    @ex(
        help='list broken load balancers',
    )
    def list(self):
        self.app.log.info('Gathering list of broken loadbalancers', __name__)
        loadbalancers = get_load_balancer_info(self, self.app.conn)
        self.app.print("Issues have been found with the following loadbalancers:")
        for loadbalancer in loadbalancers:
            self.app.render(loadbalancers[loadbalancer]['id'])


    @ex(
        help='delete broken load balancers',

        # By default, prompt for each delete, if --confirm, do not confirm
        arguments=[
            ### add '--confirm false' to suppress prompting for deletion
            ( [ '--confirm' ], {
                'help': 'Specify false to not prompt to delete each load balancer',
                'action': 'store',
                'dest': 'confirm' } ),
        ],
    )
    def delete(self):
        confirm = {
            'confirm' : True,
        }

        if self.app.pargs.confirm is not None:
            if self.app.pargs.confirm.lower() == 'false':
                confirm['confirm'] = False
            else:
                confirm['confirm'] = True

        self.app.log.info('Gathering list of broken loadbalancers', __name__)
        loadbalancers = get_load_balancer_info(self, self.app.conn)

        for loadbalancer in loadbalancers:
            if confirm['confirm'] is False:
                deleted = delete_load_balancer(self, self.app.conn, loadbalancers[loadbalancer]['id'])
            else:
                delete_it = shell.Prompt("Delete: %s ?" % loadbalancers[loadbalancer]['id'], options=['yes', 'No'], default = 'No')
                result = delete_it.prompt()
                if result.lower() == 'yes':
                    deleted = delete_load_balancer(self, self.app.conn, loadbalancers[loadbalancer]['id'])
                else:
                    self.app.log.info('Not deleting', __name__)
