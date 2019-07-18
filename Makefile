# how to read from SUFFIX env?
S := $?

all: thesis${S}

# default target
thesis${S}: ???? ??? ???

# a simple rule
multivariate_calculus${S}: univariate_calculus${S}
	touch $@
	# this is wrong, because we do not need the ${S} in the dependency list, how to remove it?
	echo $^ > $@

# or you can write...
multivariate_calculus.%: univariate_calculus.%
	touch $@
	# this is still wrong!
	echo $^ > $@

# more rules...

# clean up
clean:
	rm -r ???

# how to keep intermediate files?
.???:
