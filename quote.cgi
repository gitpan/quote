#! /usr/local/bin/perl -w


#################################################################################
#                                                                               #
#   										#
#   Quote v.0.1                                     				#
#   Copyright (c) 2002-2004 by Steven Schubiger <steven@accognoscere.org>       #
#   Last changes: 12th November 2004                                            #
#										#
#   All rights reserved.                                                        #
#                                                                               #
#   Redistribution and use in source and binary forms, with or without          #
#   modification, are permitted provided that the following conditions          #
#   are met:                                                                    #
#   1. Redistributions of source code must retain the above copyright           #
#      notice, this list of conditions and the following disclaimer.            #
#   2. Redistributions in binary form must reproduce the above copyright        #
#      notice, this list of conditions and the following disclaimer in the      #
#      documentation and/or other materials provided with the distribution.     #
#   3. The name of the author may not be used to endorse or promote products    #
#      derived from this software without specific prior written permission.    #
#                                                                               #
#   THIS SOFTWARE IS PROVIDED BY THE AUTHOR ``AS IS'' AND ANY EXPRESS OR        #
#   IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES   #
#   OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.     #
#   IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT, INDIRECT,            #
#   INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT    #
#   NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,   #
#   DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY       #
#   THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT         #
#   (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF    #
#   THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.           #
#                                                                               #
#                                                                               #
#################################################################################




# Include the configuration file
require 'quote.cfg';

use CGI::Carp ('fatalsToBrowser');


my ($mday);


&check_quoted;
&select_quote;


# The subfunction which will check if we're allowed to select a new random quote
# or if we're condemned to use the old one.
sub check_quoted {
    open (FILE_QUOTED, "<$data_dir/$quoted") or die "Could not open $data_dir/$quoted: $!";
    my $line = <FILE_QUOTED>;
    ($quote, $day_quote_issued) = $line =~ /(.*);(.*)/;
    close (FILE_QUOTED) or die "Could not close $data_dir/$quoted: $!\n";

    $mday = (localtime)[3];

    # Check if want to allow the script to update the quote
    # daily, and decide whether we're allowed to update the quote or not.
    if ($frequency == 1) {
        if ($mday != $day_quote_issued) {
            $select_quote_allowed = 1;
        } else {
            $select_quote_allowed = 0;
        }
    }

    # Check if we want to allow the script to update the quote less
    # than daily, and decide whether we're allowed to update the quote or not.
    elsif ($frequency > 1) {
        if ($mday % $frequency == 0 && $mday != $day_quote_issued) {
            $select_quote_allowed = 1;
        } elsif (! $day_quote_issued) {
            $select_quote_allowed = 1;
        } else {
            $select_quote_allowed = 0;
        }
    }
}


# The subfunction which will select a new random quote (if we're allowed to),
# and output the quote either embedded in an HTML page or just as simple text
# (depending on whether SSI is supported or not).
sub select_quote {
    # This part will be executed if we're allowed to select a new random quote
    # out of the quotes file.
    if ($select_quote_allowed) {
        open (RANDOM_QUOTES, "<$data_dir/$random_quotes") or die "Could not open $data_dir/$random_quotes: $!";
        my @random_quotes = <RANDOM_QUOTES>;
        close (RANDOM_QUOTES) or die "Could not open $data_dir/$random_quotes: $!\n";

        chomp ($quote = $random_quotes[rand $#random_quotes]);

        open (QUOTED, ">$data_dir/$quoted") or die "Could not open $data_dir/$quoted: $!\n";
        print QUOTED "$quote;$mday\n";
        close (QUOTED) or die "Could not close $data_dir/$quoted: $!\n";
    }

    # Break the quote with a newline if it gets too long to ensure that we get
    # nice HTML source code (yes, it depends :-).
    $quote =~ s/(.{50,}?) (.*)/$1 \n$2/;

    print "Content-type: text/html\n\n";
    print $quote;
    exit (0);
}