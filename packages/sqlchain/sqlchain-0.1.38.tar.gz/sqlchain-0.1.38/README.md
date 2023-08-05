### sqlChain - The Blockchain as a SQL Layer

**sqlChain** is a *compact* SQL layer that runs on top of bitcoind. It extends the query options on the blockchain with a priority placed on low storage overhead. It provides multiple API (compatible) interfaces:

- Insight API (plus some extensions, like /api/closure)
- Blockchain.info API (including websocket)
- RPC via POST, GET urls
- Web Interface (using bootstrap, integrated with API backend, primarily a demo)
- Electrum Server

A public [DEMO server](https://api.coinview.info) is now up and running - feel free to test but don't depend on it; could go down at any time and some example calls may be buggy still.

**sqlChain** currently consists of three daemon programs.

- **sqlchaind**             - monitors bitcoind and updates a mysql database
- **sqlchain-api**          - provides multiple API interfaces over the mysql database
- **sqlchain-electrum**     - runs a private electrum server over the sqlchain-api layer

#### Recent Updates

Improved sync speed with another thread to handle output inserts/updates. These can happen "out of band" with the blocks/txs as long as in order. My testing on a "hybrid" 2 Core (8GB, SSD) server showed about double the tx/s conversion rate. I'll post some test results soon when it's fully sync'd again.

Added sqlchain-init and installation guide (INSTALL.md) to help users get up and running. I've tested some more on Amazon EC2 and now also on a regular VPS account. So it's starting to get some workout and more bugs fixed. It sure runs faster on the VPS. I've found you can build a custom bitcoind and then rsync it up to the server and place in /usr/local/bin to override the default package install. That works.

Added pruning support using "manual pruning", prune=1 in bitcoin.conf. This currently requires a custom build [with PR #7871](https://github.com/bitcoin/bitcoin/pull/7871) but it's fairly painless and a better way of dealing with pruning blocks once they've been processed into MySQL. With the current blockchain size of 101 GB I'm hopeful this will cut down total storage to about half, maybe.

**sqlchain-api** now uses the gevent.websocket module to provide a low overhead, highly concurrent, WSGI based server. In theory, thousands of connections could use either the websocket, or more simply, the long polling *sync* api.

A new **blkdat** module enables syncing directly from block files. Now sqlchain can build sql data even as bitcoind syncs itself, saving a lot of time on low-end systems. 

sqlChain is still *Alpha level* software under active development (not ready for prime time) - but I'm busy on getting it there. For this reason the IRC peer discovery for public Electrum servers is not yet implemented, and wont be until enough testing has been completed.

#### TODO

- open server for demo purposes as public api - comming soon.
- more testing on Electrum server operation
- look further into pruning spent trxs (most of blob.dat) for a wallet api with even lower storage needs



