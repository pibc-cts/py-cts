# python-cts

Basic Utils of Citshares

1. In order to use this tool, please prepare the cli_wallet, and open one rpc port .
2. config the wallet_port in script.

背景介绍：
     在使用脚本之前，请先看如下的挖矿步骤：
     https://steemit.com/cts/@citshares/6jhdmn-citshares
     
     CTS和BTS的系统基本一样。重节点是整个系统的核心，也就是witness_node 这个程序。 witness_node直接通过seed-node连接。
     witness_node <------seed_node------> witness_node <-----seed_node------> witness_node
     在编译好的witness_node里默认添加了CTS的默认节点。如果需要添加额外的seed_node,可以在config.ini文件里添加：
     seed-node = xx.xx.xx.xx:10000
     
     witness_node 虽然完成了CTS系统的主要工作，但是并没有提供和用户交互的接口。和用户交互由钱包程序来完成。 witness_node开辟一个rpc端口，
     钱包程序连接上这个端口之后进行功能交互。
     
     witness_node [rpc port]  <----------------->  钱包程序
     
     witness_node开辟rpc 端口的方式如下：
     ./witness_node  --replay-blockchain   --rpc-endpoint 127.0.0.1:11010
     
     钱包程序要想连接这个端口，需要用到 -s 参数，并且加上ws://
     ./cli_wallet -s ws://127.0.0.1:11010
     
     cli_wallet是命令行钱包。它的基本操作是：
     1. 创建密码（第一次运行时）：
         new >>> set_password 123456 
     2. 解锁（每次重新打开钱包时）：
         locked >>> unlock 123456
     3. 导入账户（第一次运行时）：
          import_key  账户名  私钥 true
     4. 导入余额（第一次运行时）：
          import_balance  用户名 [私钥] true
     5. 其他操作，比如获取当前买卖单（任何时候）：
          unlocked >>> get_order_book CTS CNY 50
     
     有了cli_wallet 我们就可以完成日常所需的所有工作。但是这样还不够方便，如果想让程序自动交易，就需要使用脚本。
     cli_wallet 也可以开一个 rpc的端口，脚本去连接这个端口，然后用程序来操作cli-wallet
     
     脚本 <------rpc port------> cli_wallet
     
     cli_wallet 打开rpc 端口的方法是加-r参数：
     ./cli_wallet_1222 -s ws://127.0.0.1:11010 -r "127.0.0.1:8093"
     或者用 -H 参数也可以。
     
脚本的使用：
    上面说了，脚本是通过rpc端口来控制cli_wallet完成功能的。所以，在脚本里，第一个要修改的就是 wallet_port, 
    改成你配置的端口即可：
    wallet_port = "8093"
    
    第二个需要修改的是你的账户名字，account_name, 
    第三个是cli_wallet的密码，就是运行unlock 时的密码。
    
    其余还有常用的api，比如 market.get_order_book, account.buy等，这些可以参考cny_feedprice.py和robot.py
    具体参数就不解释了，应该都能看的懂
    
     
     
     
     
     
     
     
      
      
