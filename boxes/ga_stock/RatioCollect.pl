#!/usr/bin/perl
# take to test file want gene's data
# use strict;
# use warnings;
# written by cychen 07.12.29

#my $file_compare = '93_count_4.txt';
#my $file_ratio = 'input_test.txt';
#my $out_name='haha.txt';

my $i,$j;

my $file_compare=$ARGV[0]; #input1的檔名
my $file_ratio=$ARGV[1];	#input2的檔名
my $out_name=$ARGV[2];  #output的檔名


open (F_input1, "$file_compare")||die "can't open file_count";
open (F_input2, "$file_ratio")||die "can't open file_ratio.txt";
open (F_ouput, ">$out_name") ||die "can't open to write";

my @stock_50 = <F_input1>;
my @stock_ratio = <F_input2>;
my @output='';
my @temp='';

for($i=0;$i<@stock_50;$i++)
{
	chomp($stock_50[$i]);
	for($j=5;$j<@stock_ratio;$j++)
	{
		my @temp = split(/\t/,$stock_ratio[$j]);
		if($stock_50[$i] eq $temp[1])
		{
			push @output,$stock_50[$i]."\t".$temp[5]."\n"; #如果input2的資料是刪除過DE行，則是$temp[3]
		}
		if($stock_50[$i] eq $temp[12])
		{
			push @output,$stock_50[$i]."\t".$temp[16]."\n";
		}
	}
}

print F_ouput @output;

close F_input1;
close F_input2;
close F_ouput;