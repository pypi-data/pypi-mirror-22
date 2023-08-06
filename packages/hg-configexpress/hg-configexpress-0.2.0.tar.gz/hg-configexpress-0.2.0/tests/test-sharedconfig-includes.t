initialize repositories
  $ hg init serverrepo2
  $ touch serverrepo2/a
  $ hg -R serverrepo2 add serverrepo2/a
  $ hg -R serverrepo2 commit -ma
  $ hg clone -U serverrepo2 clientrepo

  $ cat >> $HGRCPATH << EOF
  > [ui]
  > ssh=python "$RUNTESTDIR/dummyssh"
  > [extensions]
  > configexpress = $(dirname $TESTDIR)/hgext3rd/configexpress.py
  > [section_a]
  > entry1 = foo
  > entry2 = barbar
  > [section_b]
  > someentry = sometext
  > otherentry = test
  > EOF

check includes proposed by the server
  $ cat > serverrepo2/.hg/hgrc << EOF
  > [configexpress:server2client]
  > fooconfig = configproposal
  > fooconfig:type = includes
  > fooconfig:selection = all
  > EOF
  $ cat > serverrepo2/.hg/configproposal << EOF
  > foo.rc
  > 
  > bar.rc
  > EOF
  $ cat > clientrepo/.hg/hgrc << EOF
  > %include bar.rc
  > EOF
  $ touch clientrepo/.hg/bar.rc
  $ hg -R clientrepo pull serverrepo2
  pulling from serverrepo2
  searching for changes
  no changes found
  the following includes are missing in your configuration:
    %include foo.rc
  (add the above lines to your hgrc to fix your configuration)

check missing last include (edge case)
  $ cat > clientrepo/.hg/hgrc << EOF
  > %include foo.rc
  > EOF
  $ touch clientrepo/.hg/foo.rc
  $ hg -R clientrepo pull serverrepo2
  pulling from serverrepo2
  searching for changes
  no changes found
  the following includes are missing in your configuration:
    %include bar.rc
  (add the above lines to your hgrc to fix your configuration)

check absolute includes
  $ cat > serverrepo2/.hg/configproposal << EOF
  > $TESTTMP/meh.rc
  > $TESTTMP/moh.rc
  > EOF
  $ cat > clientrepo/.hg/hgrc << EOF
  > %include $TESTTMP/meh.rc
  > EOF
  $ touch $TESTTMP/meh.rc
  $ hg -R clientrepo pull serverrepo2
  pulling from serverrepo2
  searching for changes
  no changes found
  the following includes are missing in your configuration:
    %include $TESTTMP/moh.rc
  (add the above lines to your hgrc to fix your configuration)

check includes in subdirectories
  $ mkdir serverrepo2/.hg/subdir
  $ mv serverrepo2/.hg/hgrc serverrepo2/.hg/hgrc.backup
  $ cat > serverrepo2/.hg/hgrc << EOF
  > [configexpress:server2client]
  > fooconfig = subdir/configproposal
  > fooconfig:type = includes
  > fooconfig:selection = all
  > EOF
  $ mv serverrepo2/.hg/configproposal serverrepo2/.hg/subdir/configproposal
  $ hg -R clientrepo pull serverrepo2
  pulling from serverrepo2
  searching for changes
  no changes found
  the following includes are missing in your configuration:
    %include $TESTTMP/moh.rc
  (add the above lines to your hgrc to fix your configuration)

(restore config)
  $ mv serverrepo2/.hg/hgrc.backup serverrepo2/.hg/hgrc
  $ cat > serverrepo2/.hg/configproposal << EOF
  > foo.rc
  > bar.rc
  > EOF
  $ cat > clientrepo/.hg/hgrc << EOF
  > %include bar.rc
  > EOF

(with an option, one of the includes is enough)
  $ cat > serverrepo2/.hg/hgrc << EOF
  > [configexpress:server2client]
  > fooconfig = configproposal
  > fooconfig:type = includes
  > fooconfig:selection = any
  > EOF
  $ hg -R clientrepo pull serverrepo2
  pulling from serverrepo2
  searching for changes
  no changes found
  $ rm clientrepo/.hg/bar.rc clientrepo/.hg/hgrc
  $ hg -R clientrepo pull serverrepo2
  pulling from serverrepo2
  searching for changes
  no changes found
  you need at least one of the following includes in your configuration:
    %include foo.rc
    %include bar.rc
  (add one of the above lines to your hgrc to fix your configuration)

(missing selection parameter)
  $ cat > serverrepo2/.hg/hgrc << EOF
  > [configexpress:server2client]
  > fooconfig = configproposal
  > fooconfig:type = includes
  > EOF
  $ hg -R clientrepo pull serverrepo2
  pulling from serverrepo2
  searching for changes
  no changes found
  the following includes are missing in your configuration:
    %include foo.rc
    %include bar.rc
  (add the above lines to your hgrc to fix your configuration)

  $ cat > serverrepo2/.hg/hgrc << EOF
  > [configexpress:server2client]
  > fooconfig = configproposal
  > fooconfig:type = includes
  > fooconfig:selection = all
  > EOF
  $ hg -R clientrepo pull serverrepo2
  pulling from serverrepo2
  searching for changes
  no changes found
  the following includes are missing in your configuration:
    %include foo.rc
    %include bar.rc
  (add the above lines to your hgrc to fix your configuration)
  $ cat >> clientrepo/.hg/hgrc << EOF
  > [configexpress:server2client]
  > fooconfig:ignore = True
  > EOF
  $ hg -R clientrepo pull serverrepo2
  pulling from serverrepo2
  searching for changes
  no changes found
  $ cat >> clientrepo/.hg/hgrc << EOF
  > [configexpress:server2client]
  > fooconfig:ignore = False
  > EOF
  $ hg -R clientrepo pull serverrepo2
  pulling from serverrepo2
  searching for changes
  no changes found
  the following includes are missing in your configuration:
    %include foo.rc
    %include bar.rc
  (add the above lines to your hgrc to fix your configuration)
