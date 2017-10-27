<?php
class WebsocketTest {
    public $server;
    public function __construct() {
        $this->server = new swoole_websocket_server("0.0.0.0", 9999);
        $this->server->on('open', function (swoole_websocket_server $server, $request) {
                echo "server: handshake success with fd{$request->fd}\n";
            });
        $this->server->on('message', function (swoole_websocket_server $server, $frame) {
                echo "receive from {$frame->fd}:{$frame->data},opcode:{$frame->opcode},fin:{$frame->finish}\n";
                $server->push($frame->fd, "this is server");
            });
        $this->server->on('close', function ($ser, $fd) {
                echo "client {$fd} closed\n";
            });
        $this->server->on('request', function ($request, $response) {
                // 接收http请求从get获取message参数的值，给用户推送
                // $this->server->connections 遍历所有websocket连接用户的fd，给所有用户推送
                foreach ($this->server->connections as $fd) {
                    $this->server->push($fd, $request->get['message']);
                }
            });
        // $context=new ZMQContext();
        // $subscriber = new ZMQSocket($context, ZMQ::SOCKET_SUB);
        // $subscriber->connect("tcp://192.168.31.4:5555");
        // $subscriber->setSockOpt(ZMQ::SOCKOPT_SUBSCRIBE, "");
        $this->server->start();
    }
}
echo 'hello world';
$ws=new WebsocketTest();
