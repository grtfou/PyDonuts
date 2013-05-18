#!/usr/bin/perl
#############################
# GA paper   by cychen  08.02.25
#############################
# use strict;
# use warnings;

my $input_file="t1-3-20.txt";	#��J�������
my $chromosome_num=100;		#�V�����
my $crossover_rate=0.2;		#��t�v
my $mutation_rate=0.001;	#���ܲv
my $run_time=100;			#�]������

system("perl ga_strategy2.pl $input_file $chromosome_num $crossover_rate $mutation_rate $run_time");
#########
my $ga_answer="$chromosome_num�V����_$crossover_rate��t�v_$mutation_rate���ܲv_$run_time�@�N����.txt";
my $file_rewind="rewind.txt";

open (F_gaAnswer_inf, "$ga_answer")||die "can't open rewind's information file\n";
open (F_rewind_inf, "$file_rewind")||die "can't open rewind's information file\n";
my @gaAnswer_inf=<F_gaAnswer_inf>;
my @rewind_inf=<F_rewind_inf>;
#########

### �p����S�v ###
my @gaAnswer_temp=();
my @rewind_temp=();
@gaAnswer_temp=split(/\t/,$gaAnswer_inf[0]);
@rewind_temp=split(/\t/,$rewind_inf[0]);

my $rewind_total=0;
for(my $i=0;$i<@rewind_temp;++$i)
{
	$rewind_total+=$gaAnswer_temp[$i]*$rewind_temp[$i];
}
$rewind_total=sprintf("%.3f",$rewind_total*100);
print "�������S�v".$rewind_total."%\n\n";
##** end �p����S�v ###

close(F_gaAnswer_inf);
close(F_rewind_inf);

system("pause");
