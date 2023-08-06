#require killdaemons

prepare serverhook to show config that was sent
  $ cat >> serverhook.py << EOF
  > def ourserverhook(ui, repo, **kwargs):
  >     for (k, v) in sorted(kwargs.items()):
  >         if k == 'hgversion' or k.startswith('config_'):
  >             print('hookarg: %s - %s' % (k, v))
  >     return True
  > EOF
  $ export PYTHONPATH=$TESTTMP:$PYTHONPATH

  $ cat >> $HGRCPATH << EOF
  > [ui]
  > ssh=python "$RUNTESTDIR/dummyssh"
  > [extensions]
  > configexpress = $(dirname $TESTDIR)/hgext3rd/configexpress.py
  > [configexpress]
  > share-repo-format = yes
  > [section_a]
  > entry1 = foo
  > entry2 = barbar
  > [section_b]
  > someentry = sometext
  > otherentry = test
  > EOF

setup server

  $ hg init serverrepo --traceback
  $ cat >> serverhgrc << EOF
  > [hooks]
  > pretxnchangegroup.serverhook = printenv.py pretxnchangegroup 0
  > pretxnclose.serverhook = printenv.py pretxnclose 1
  > EOF
  $ cp serverhgrc serverrepo/.hg/hgrc
  $ hg init clientrepo
  $ cd clientrepo
  $ echo a > a
  $ hg add a
  $ hg commit -m A0
  $ echo b > b
  $ hg add b
  $ hg commit -m B0
  $ cd ..

setup clients

  $ hg clone --pull serverrepo client-up-to-date
  no changes found
  updating to branch default
  0 files updated, 0 files merged, 0 files removed, 0 files unresolved
  $ hg clone --pull serverrepo --config format.usedotencode=no --config format.generaldelta=no client-multiple-deficiencies
  no changes found
  updating to branch default
  0 files updated, 0 files merged, 0 files removed, 0 files unresolved

check value on push

  $ cd client-up-to-date
  $ echo c > c
  $ hg add c
  $ hg commit -m C0

#if hg42

  $ hg push
  pushing to $TESTTMP/serverrepo
  searching for changes
  adding changesets
  adding manifests
  adding file changes
  added 1 changesets with 1 changes to 1 files
  pretxnchangegroup hook: HG_BUNDLE2=1 HG_CLIENTCONFIG_HGVERSION=* HG_CLIENTFORMAT_DOTENCODE__CONFIG=1 HG_CLIENTFORMAT_DOTENCODE__DEFAULT=1 HG_CLIENTFORMAT_DOTENCODE__REPO=1 HG_CLIENTFORMAT_FNCACHE__CONFIG=1 HG_CLIENTFORMAT_FNCACHE__DEFAULT=1 HG_CLIENTFORMAT_FNCACHE__REPO=1 HG_CLIENTFORMAT_GENERALDELTA__CONFIG=1 HG_CLIENTFORMAT_GENERALDELTA__DEFAULT=1 HG_CLIENTFORMAT_GENERALDELTA__REPO=1 HG_CLIENTFORMAT_REMOVECLDELTACHAIN__CONFIG=1 HG_CLIENTFORMAT_REMOVECLDELTACHAIN__DEFAULT=1 HG_CLIENTFORMAT_REMOVECLDELTACHAIN__REPO=1 HG_HOOKNAME=pretxnchangegroup.serverhook HG_HOOKTYPE=pretxnchangegroup HG_NODE=c16e6831ba746fab3b7297bd9f95bd4832d5dd2e HG_NODE_LAST=c16e6831ba746fab3b7297bd9f95bd4832d5dd2e HG_PENDING=$TESTTMP/serverrepo HG_SOURCE=push HG_TXNID=TXN:$ID$ HG_URL=file:$TESTTMP/serverrepo (glob)
  pretxnclose hook: HG_BUNDLE2=1 HG_CLIENTCONFIG_HGVERSION=* HG_CLIENTFORMAT_DOTENCODE__CONFIG=1 HG_CLIENTFORMAT_DOTENCODE__DEFAULT=1 HG_CLIENTFORMAT_DOTENCODE__REPO=1 HG_CLIENTFORMAT_FNCACHE__CONFIG=1 HG_CLIENTFORMAT_FNCACHE__DEFAULT=1 HG_CLIENTFORMAT_FNCACHE__REPO=1 HG_CLIENTFORMAT_GENERALDELTA__CONFIG=1 HG_CLIENTFORMAT_GENERALDELTA__DEFAULT=1 HG_CLIENTFORMAT_GENERALDELTA__REPO=1 HG_CLIENTFORMAT_REMOVECLDELTACHAIN__CONFIG=1 HG_CLIENTFORMAT_REMOVECLDELTACHAIN__DEFAULT=1 HG_CLIENTFORMAT_REMOVECLDELTACHAIN__REPO=1 HG_HOOKNAME=pretxnclose.serverhook HG_HOOKTYPE=pretxnclose HG_NODE=c16e6831ba746fab3b7297bd9f95bd4832d5dd2e HG_NODE_LAST=c16e6831ba746fab3b7297bd9f95bd4832d5dd2e HG_PENDING=$TESTTMP/serverrepo HG_SOURCE=push HG_TXNID=TXN:$ID$ HG_TXNNAME=push HG_URL=file:$TESTTMP/serverrepo (glob)
  transaction abort!
  rollback completed
  abort: pretxnclose.serverhook hook exited with status 1
  [255]

#else

  $ hg push
  pushing to $TESTTMP/serverrepo
  searching for changes
  cannot send repository format data to the server, Mercurial version too old
  (upgrade to Mercurial 4.2+ or set config.express.share-repo-format=no)
  adding changesets
  adding manifests
  adding file changes
  added 1 changesets with 1 changes to 1 files
  pretxnchangegroup hook: HG_BUNDLE2=1 HG_CLIENTCONFIG_HGVERSION=* HG_NODE=c16e6831ba746fab3b7297bd9f95bd4832d5dd2e HG_NODE_LAST=c16e6831ba746fab3b7297bd9f95bd4832d5dd2e HG_PENDING=$TESTTMP/serverrepo HG_SOURCE=push HG_TXNID=TXN:* HG_URL=file:$TESTTMP/serverrepo (glob)
  pretxnclose hook: HG_BUNDLE2=1 HG_CLIENTCONFIG_HGVERSION=* HG_NODE=c16e6831ba746fab3b7297bd9f95bd4832d5dd2e HG_NODE_LAST=c16e6831ba746fab3b7297bd9f95bd4832d5dd2e HG_PENDING=$TESTTMP/serverrepo HG_SOURCE=push HG_TXNID=TXN:* HG_TXNNAME=push HG_URL=file:$TESTTMP/serverrepo (glob)
  transaction abort!
  rollback completed
  abort: pretxnclose.serverhook hook exited with status 1
  [255]

#endif

  $ cd ..

  $ cd client-multiple-deficiencies
  $ hg pull
  pulling from $TESTTMP/serverrepo
  no changes found
  $ hg update
  0 files updated, 0 files merged, 0 files removed, 0 files unresolved
  $ echo d > d
  $ hg add d
  $ hg commit -m D0

#if hg42

  $ hg push
  pushing to $TESTTMP/serverrepo
  searching for changes
  adding changesets
  adding manifests
  adding file changes
  added 1 changesets with 1 changes to 1 files
  pretxnchangegroup hook: HG_BUNDLE2=1 HG_CLIENTCONFIG_HGVERSION=* HG_CLIENTFORMAT_DOTENCODE__CONFIG=1 HG_CLIENTFORMAT_DOTENCODE__DEFAULT=1 HG_CLIENTFORMAT_DOTENCODE__REPO=1 HG_CLIENTFORMAT_FNCACHE__CONFIG=1 HG_CLIENTFORMAT_FNCACHE__DEFAULT=1 HG_CLIENTFORMAT_FNCACHE__REPO=1 HG_CLIENTFORMAT_GENERALDELTA__CONFIG=1 HG_CLIENTFORMAT_GENERALDELTA__DEFAULT=1 HG_CLIENTFORMAT_GENERALDELTA__REPO=1 HG_CLIENTFORMAT_REMOVECLDELTACHAIN__CONFIG=1 HG_CLIENTFORMAT_REMOVECLDELTACHAIN__DEFAULT=1 HG_CLIENTFORMAT_REMOVECLDELTACHAIN__REPO=1 HG_HOOKNAME=pretxnchangegroup.serverhook HG_HOOKTYPE=pretxnchangegroup HG_NODE=fa243c4bbcfdc0f6015597bf601c762e966c8da1 HG_NODE_LAST=fa243c4bbcfdc0f6015597bf601c762e966c8da1 HG_PENDING=$TESTTMP/serverrepo HG_SOURCE=push HG_TXNID=TXN:$ID$ HG_URL=file:$TESTTMP/serverrepo (glob)
  pretxnclose hook: HG_BUNDLE2=1 HG_CLIENTCONFIG_HGVERSION=* HG_CLIENTFORMAT_DOTENCODE__CONFIG=1 HG_CLIENTFORMAT_DOTENCODE__DEFAULT=1 HG_CLIENTFORMAT_DOTENCODE__REPO=1 HG_CLIENTFORMAT_FNCACHE__CONFIG=1 HG_CLIENTFORMAT_FNCACHE__DEFAULT=1 HG_CLIENTFORMAT_FNCACHE__REPO=1 HG_CLIENTFORMAT_GENERALDELTA__CONFIG=1 HG_CLIENTFORMAT_GENERALDELTA__DEFAULT=1 HG_CLIENTFORMAT_GENERALDELTA__REPO=1 HG_CLIENTFORMAT_REMOVECLDELTACHAIN__CONFIG=1 HG_CLIENTFORMAT_REMOVECLDELTACHAIN__DEFAULT=1 HG_CLIENTFORMAT_REMOVECLDELTACHAIN__REPO=1 HG_HOOKNAME=pretxnclose.serverhook HG_HOOKTYPE=pretxnclose HG_NODE=fa243c4bbcfdc0f6015597bf601c762e966c8da1 HG_NODE_LAST=fa243c4bbcfdc0f6015597bf601c762e966c8da1 HG_PENDING=$TESTTMP/serverrepo HG_SOURCE=push HG_TXNID=TXN:$ID$ HG_TXNNAME=push HG_URL=file:$TESTTMP/serverrepo (glob)
  transaction abort!
  rollback completed
  abort: pretxnclose.serverhook hook exited with status 1
  [255]

#else

  $ hg push
  pushing to $TESTTMP/serverrepo
  searching for changes
  cannot send repository format data to the server, Mercurial version too old
  (upgrade to Mercurial 4.2+ or set config.express.share-repo-format=no)
  adding changesets
  adding manifests
  adding file changes
  added 1 changesets with 1 changes to 1 files
  pretxnchangegroup hook: HG_BUNDLE2=1 HG_CLIENTCONFIG_HGVERSION=* HG_NODE=fa243c4bbcfdc0f6015597bf601c762e966c8da1 HG_NODE_LAST=fa243c4bbcfdc0f6015597bf601c762e966c8da1 HG_PENDING=$TESTTMP/serverrepo HG_SOURCE=push HG_TXNID=TXN:* HG_URL=file:$TESTTMP/serverrepo (glob)
  pretxnclose hook: HG_BUNDLE2=1 HG_CLIENTCONFIG_HGVERSION=* HG_NODE=fa243c4bbcfdc0f6015597bf601c762e966c8da1 HG_NODE_LAST=fa243c4bbcfdc0f6015597bf601c762e966c8da1 HG_PENDING=$TESTTMP/serverrepo HG_SOURCE=push HG_TXNID=TXN:* HG_TXNNAME=push HG_URL=file:$TESTTMP/serverrepo (glob)
  transaction abort!
  rollback completed
  abort: pretxnclose.serverhook hook exited with status 1
  [255]

#endif

  $ cd ..
