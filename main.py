from dnslib import *
from dnslib.server import *
import sys
import time
from common.fsdserver import get_nearest_server

class TestResolver:
    def resolve(self, request, handler):
        # 用户本身的ip
        userip = handler.client_address[0]
        reply = request.reply()
        qname = request.q.qname
        qtype = request.q.qtype
        print(qname, qtype, userip)
        if qname == 'sim.trish.top' and QTYPE[qtype] == 'A':
            print(get_nearest_server(userip))
            answer = RR(rname=qname, ttl=60, rdata=A('182.150.1.25'))
            reply.add_answer(answer)
            return reply
        ## 调价其他的域名对应的IP，在这里加if语句增加

        ## 未匹配到时的返回值
        reply.header.rcode = getattr(RCODE, 'NXDOMAIN')
        return reply


def main():
    resolver = TestResolver()
    logger = DNSLogger(prefix=False)
    dns_server = DNSServer(resolver, port=53, address='0.0.0.0', logger=logger)
    dns_server.start_thread()
    try:
        while True:
            time.sleep(600)
            sys.stderr.flush()
            sys.stdout.flush()
    except KeyboardInterrupt:
        sys.exit(0)


if __name__ == '__main__':
    main()



