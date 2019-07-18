# how to read from SUFFIX env?
S := $?

# default target
thesis${S}: ???? ??? ???

# a simple rule
multivariate_calculus${S}: univariate_calculus${S}
	touch $@
	# this is wrong, because we do not need the ${S} in the dependency list, how to remove it?
	echo $^ > $@

# more rules...

# clean up
clean:
	rm -r ???
