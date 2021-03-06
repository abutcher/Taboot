#!/usr/bin/make

ASCII2MAN = a2x -D $(dir $@) -d manpage -f manpage $<
ASCII2HTMLMAN = a2x -D docs/html/man/ -d manpage -f xhtml
NAME := python-taboot
VERSION := $(shell cat VERSION)
RELEASE := $(shell awk '/Release/{print $$2}' < python-taboot.spec | cut -d "%" -f1)
CURVERSION := $(shell python -c "import taboot; print taboot.__version__")
FULLNAME = $(NAME)-$(VERSION)
MANPAGES := docs/man/man1/taboot.1 docs/man/man5/taboot-tasks.5
DOCPATH := /usr/share/doc/$(NAME)
SITELIB = $(shell python -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")

viewdoc: docs
	python ./setup.py viewdoc

docs: manuals htmldocs htmlman

manuals: $(MANPAGES)

%.1: %.1.asciidoc
	$(ASCII2MAN)

%.5: %.5.asciidoc
	$(ASCII2MAN)

htmlman:
	mkdir -p docs/html/man
	$(ASCII2HTMLMAN) docs/man/man1/taboot.1.asciidoc
	$(ASCII2HTMLMAN) docs/man/man5/taboot-tasks.5.asciidoc

htmldocs:
	./setup.py doc

install:
	./setup.py install

installdocs: docs
	mkdir -p /usr/share/doc/$(NAME)
	cp -r docs/rst $(DOCPATH)
	cp -r docs/html $(DOCPATH)
	gzip -c docs/man/man1/taboot.1 > /usr/share/man/man1/taboot.1.gz
	gzip -c docs/man/man5/taboot-tasks.5 > /usr/share/man/man5/taboot-tasks.5.gz

uninstall:
	rm -fR /usr/share/doc/$(NAME)
	rm -f /usr/share/man/man1/taboot.1.gz
	rm -f /usr/share/man/man5/taboot.5.gz
	rm -fR $(SITELIB)/taboot-func/
	rm -fR $(SITELIB)/taboot/
	rm -f /usr/bin/taboot

version:
	@echo $(VERSION)

testdist: clean
	tito build --test --tgz

sdist: clean
	@echo "Remember that you should only sdist if you've tagged this release first."
	tito build --tgz

srpm: clean
	@echo "Remember that you shold only srpm if you've tagged this release first."
	tito build --srpm

rpm:
	@echo "Remember that you should only rpm if you've tagged this release first."
	tito build --rpm

tag: clean
	tito tag

release:
	@echo $(RELEASE)

testrelease:
# Like a release but in a "build --test" kind of way.
	tito build --test --rpm

clean:
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*~" -delete
	find ./docs/ -type f -name "*.xml" -delete
	find . -type f -name "#*" -delete
	rm -fR docs/.doctrees docs/html dist build

.PHONEY: docs manual htmldoc clean version release sdist
vpath %.asciidoc docs/man/man1 docs/man/man5
