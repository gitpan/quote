#! /usr/local/bin/perl -w


#################################################################################
#										#
#  										#
#   Quote v.0.2							       	        #
#   Copyright (C) 2003-2004 - Steven Schubiger <steven@accognoscere.org>	#
#   Last changes: 12th November 2004						#
#										#
#   This program is free software; you can redistribute it and/or modify	#
#   it under the terms of the GNU General Public License as published by	#
#   the Free Software Foundation; either version 2 of the License, or		#
#   (at your option) any later version.						#
#										#
#   This program is distributed in the hope that it will be useful,		#
#   but WITHOUT ANY WARRANTY; without even the implied warranty of		#
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the		#
#   GNU General Public License for more details.				#
#										#
#   You should have received a copy of the GNU General Public License		#
#   along with this program; if not, write to the Free Software			#
#   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA	#
#										#
#										#
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