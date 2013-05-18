#!/usr/bin/perl
#############################
# GA paper   by cychen  08.02.15
# ��J���:�ѦW,���S,���I
# fitness function = Sharp Ratio = ���S / ���I
#############################
# use strict;
# use warnings;

#�Ѳ���T���ɦW
chomp(my $file_stock_inf=$ARGV[0]);
open (F_stock_inf, "$file_stock_inf")||die "can't open stock's information file\n";
my @stock_inf_total=<F_stock_inf>;

#�Q�n���ͦh�ּƶq���V����
chomp(my $chromosome_count = $ARGV[1]);				#�V�����(�Ѳ�������t�������Ӽ�)
#��t�v(crossover rate)[��J0~1�������Ʀr]:
chomp(my $crossover_rate = $ARGV[2]);				#��t�v(�C���V����h�־��v�|�Q��t)
#���ܲv(crossover rate)[��J0~1�������Ʀr]:
chomp(my $mutation_rate = $ARGV[3]);				#���ܲv(�`��]�Ʀ��h�֤�ҷ|�Q����)
#�̤j�|�N����(�������):
chomp(my $run_time = $ARGV[4]);						#�p�G�����ব���A�̦h�]�X��
#print "�@�N�����t����(�������)[��J0~1�������Ʀr]:";
#chomp(my $difference_rang = <STDIN>);						#�p�G�����A�O���N��W�@�N�t���t�b�h�֤���

###########################�����ܼư�########################################
### �����V���骺�������S�έ��I ###
	my @sharpRatio=();
### ����chromosome ###
	my $gene_count=$#stock_inf_total; #�C���V���餤����](�Ѳ�)��
	my @chromosome_cluster=();
### �i��A����ƪ��B�� ###
	my @fitnessFunction=();
	my $chromosome_num=0;			#��chromosome_cluster���p��
### �Ƨ�(�ƦW��) ###
	my @temp_fitnessFunction=();	#�ȦsfitnessFunction�Ƨǫᵲ�G
	my $fitnessFunction_vs=0;
	my @last_chromosome=();
	my @over_cross=();				#��t���᪺�V����
	my @over_mutation=();			#���ܧ��᪺�V����
	my @over_normalization=();		#���W�Ƨ����V����
	my @OldNice_chromosome=();		#�e�@�N�̨Ϊ��V����
	my @ThisNice_chromosome=();		#���N��t���ܧ����V����
	my @TheNew_chromosome=();		#�s�@�N�V����

##########################################################################
for(my $now_runTime=0;$now_runTime<$run_time;++$now_runTime)
{
#$file_write="nice_answer$now_runTime.txt";
#open (F_output, ">$file_write") || die "can't output answer file\n";
	if($now_runTime==0)
	{
		cal_chromo_AvgCash_Risk();	### �����V���骺�������S�έ��I ### in:��J��; out:@sharpRatio
		create_chromosome();		###���ͷs���V���� ### out:@chromosome_cluster
	}
	cal_fitness_function(@chromosome_cluster);		### �i��A����ƪ��B�� ### in:�V����s; out:@fitnessFunction
	sort_fitness_function(10,@fitnessFunction);		### �Ƨ�(�ƦW��) �A�Ĥ@��ѼƥN��n��e�ʤ����X ### in:@fitnessFunction; out:$fitnessFunction_vs
	@OldNice_chromosome=Selection();				### �W�W�@�N�̦n����^ ### in:@chromosome_cluster,$fitnessFunction_vs

	#print "-------------------����t�e------------------------\n";
	@last_chromosome=@chromosome_cluster;
	@over_cross=crossover();						### in:@last_chromosome
	@over_generation=mutation();					### in:@over_cross
	#@over_normalization=normalization(@over_mutation);
	#print "-------------------���@�N����--------------------\n";
	#print @over_normalization;
	#@over_generation=@over_normalization;

	@fitnessFunction=();
	$fitnessFunction_vs=0;
	@chromosome_cluster=@over_generation;
	cal_fitness_function(@over_generation);			### �i��A����ƪ��B�� ### in:�V����s; out:@fitnessFunction
	sort_fitness_function(90,@fitnessFunction);		### �Ƨ�(�ƦW��) �A�Ĥ@��ѼƥN��n��e�ʤ����X ### in:@fitnessFunction; out:$fitnessFunction_vs
	@ThisNice_chromosome=Selection();				### ��t���ܫ᥻�N�̦n����^ ### in:@chromosome_cluster,$fitnessFunction_vs

	@TheNew_chromosome=();
	push @TheNew_chromosome,@OldNice_chromosome;
	push @TheNew_chromosome,@ThisNice_chromosome;
	@TheNew_chromosome=normalization(@TheNew_chromosome);

	@fitnessFunction=();
	$fitnessFunction_vs=0;
	#@chromosome_cluster=@over_generation;
	@chromosome_cluster=@TheNew_chromosome;
	cal_fitness_function(@TheNew_chromosome);		### �i��A����ƪ��B��  ### in:�V����s; out:@fitnessFunction
	sort_fitness_function(100,@fitnessFunction);	### �Ƨ�(�ƦW��) �A�Ĥ@��ѼƥN��n��e�ʤ����X ### in:@fitnessFunction; out:$fitnessFunction_vs
	@TheNew_chromosome=Selection();					### ���N�V���� ### in:@chromosome_cluster,$fitnessFunction_vs

	### ��X�̨Ϊ��A����Ƭ��h�� ###
	my @this_temp_fitnessFunction=@fitnessFunction;	#�ȦsfitnessFunction�Ƨǫᵲ�G
	for(my $i=0;$i<$chromosome_count;++$i)
	{
		for(my $j=0;$j<$chromosome_count;++$j)
		{
			if($this_temp_fitnessFunction[$i]>$this_temp_fitnessFunction[$j])
			{
				my $temp=0;
				$temp=$this_temp_fitnessFunction[$i];
				$this_temp_fitnessFunction[$i]=$this_temp_fitnessFunction[$j];
				$this_temp_fitnessFunction[$j]=$temp;
			}
		}
	}
	##**end ��X�̨Ϊ��A����Ƭ��h�� ###

	my $temp_runTime=$now_runTime+1;
	print "\n ��$temp_runTime�@�N��_�Ĥ@�W�A����� $this_temp_fitnessFunction[0]";
	print "==============���@�N����====================\n";

	##�L�X������t���զX
	if($now_runTime==$run_time-1)
	{
		$file_write="Generation $run_time.txt";
		open (F_output, ">$file_write") || die "can't output answer file\n";

		my $temp_num=0;
		for(my $f=0;$f<$chromosome_count;++$f)
		{
			for(my $g=0;$g<$gene_count;++$g)
			{
				print F_output $TheNew_chromosome[$temp_num]."\t";
				++$temp_num;
			}
			print F_output "$fitnessFunction[$f]";

			### �L�X�̨Ϊ��V���� ###
			if ($this_temp_fitnessFunction[0]==$fitnessFunction[$f])
			{
				my $file_niceout="$ARGV[1]�V����_$ARGV[2]��t�v_$ARGV[3]���ܲv_$ARGV[4]�@�N����.txt";
				open (F_outnice, ">$file_niceout") || die "can't output answer file\n";

				for(my $h=0;$h<$gene_count;++$h)
				{
					#print $TheNew_chromosome[$f*$gene_count+$h]."\t";
					print F_outnice $TheNew_chromosome[$f*$gene_count+$h]."\t";
				}
			}
			close (F_outnice);
			##**end �L�X�̨Ϊ��V���� ###
		}
		close(F_output);
	}
	@fitnessFunction=();
	@chromosome_cluster=@TheNew_chromosome;
}
close(F_stock_inf);


### �����V���骺�������S�έ��I ###
sub cal_chromo_AvgCash_Risk()
{
	my $ave_increment=0;	#�������S
	my $risk=0;			#���I
	my $sharp_ratio=0; 	#�A����ơA�ĥ�sharp��v
	@sharpRatio=();
	for(my $i=1;$i<@stock_inf_total;++$i)
	{
		my @temp=();
		@temp=split(/\t/,$stock_inf_total[$i]);
		for(my $j=1;$j<@temp;++$j)
		{
			if($j<=@temp-2)
			{
				$ave_increment+=$temp[$j];
			}
			elsif ($j==@temp-1)
			{
				$risk=$temp[$j];
			}
		}
		$ave_increment/=(@temp-2);
		#print $ave_increment."\n";
		#print $risk."\n";

		$sharp_ratio=$ave_increment/$risk;
		push @sharpRatio,$sharp_ratio;

		$ave_increment=0;
		$risk=0;
	}
}
##**end �����V���骺�������S�έ��I ###

### ����chromosome ###
sub create_chromosome
{
	@chromosome_cluster=();
	for(my $count1=1;$count1<=$chromosome_count;$count1++)
	{
		my @chromosome =();
		my $gene=0;
		for(my $i=1;$i<=$gene_count;++$i)
		{
			$gene = sprintf "%.3f", rand(1);#$cash_ratio_surplus); #������t����v�üƨM�w�A����p�ƲĤT��
			push @chromosome,$gene;
		}
		push @chromosome_cluster,@chromosome;
		#print @chromosome;
		#print "\n";
	}
}
##**end ����chromosome ###

### �i��A����ƪ��B�� ###
sub cal_fitness_function
{
	my (@cal_temp_chromosome)=@_;
	@fitnessFunction=();
	$chromosome_num=0;	#��chromosome_cluster���p��
	for(my $count2=1;$count2<=$chromosome_count;$count2++)
	{
		my $fitness_function=0;
		for(my $i=0;$i<$gene_count;++$i)
		{
			my $one_stock_fit=0;
			$one_stock_fit=$cal_temp_chromosome[$chromosome_num]*$sharpRatio[$i];
			$fitness_function+=$one_stock_fit;
			#print $one_stock_fit,"\n";
			#print $chromosome_num,$i,"\n";
			++$chromosome_num;
		}
		push @fitnessFunction,$fitness_function."\n";
	}
	#print @fitnessFunction;
	#print "\n";
}
##**end �i��A����ƪ��B�� ###

### �Ƨ�(�ƦW��) ###
sub sort_fitness_function
{
	my ($wantRate,@wantToSort)=@_;		# �Q�n�ƧǪ�fitness_function�}�C
	$fitnessFunction_vs=0;
	@temp_fitnessFunction=@wantToSort;	#�ȦsfitnessFunction�Ƨǫᵲ�G
	for(my $i=0;$i<$chromosome_count;++$i)
	{
		for(my $j=0;$j<$chromosome_count;++$j)
		{
			if($temp_fitnessFunction[$i]>$temp_fitnessFunction[$j])
			{
				my $temp=0;
				$temp=$temp_fitnessFunction[$i];
				$temp_fitnessFunction[$i]=$temp_fitnessFunction[$j];
				$temp_fitnessFunction[$j]=$temp;
			}
		}
	}
	#fintnessFunction �e�ʤ����h�� �P ��ʤ����h�֪����ӰϹj�Ʀr(�ʤ���50���ܡA�N�O�������)
	$fitnessFunction_vs=$temp_fitnessFunction[int(($chromosome_count*$wantRate/100)-1)];
	#print @fitnessFunction;
	#print @temp_fitnessFunction;
	#print "\n";
	#print $fitnessFunction_vs;
}
##**end �Ƨ�(�ƦW��) ###

############################################
### ��� ###
sub Selection
{
	my @temp_new_chromosome=();
	$chromosome_num=0;
	for(my $i=0;$i<$chromosome_count;++$i)
	{
		if($fitnessFunction[$i]>=$fitnessFunction_vs)
		{
			for(my $j=0;$j<$gene_count;++$j)
			{
				push @temp_new_chromosome,$chromosome_cluster[$chromosome_num];
				#print $chromosome_cluster[$chromosome_num]."\n";
				++$chromosome_num;
			}
		}
		else
		{
			$chromosome_num=$chromosome_num+$gene_count;
		}
		#print "\n";
	}
	return @temp_new_chromosome;
}
##**end ��� ###

## �ƻs�G���N=�e�@�N+�o�@�N�A�p�G�O�Ĥ@�N�A�N���N=�Ĥ@�N+�Ĥ@�N ###
sub CopyChromosome
{
	my (@get_addChromosome)=@_;
	my @temp_copy_chromosome=@get_addChromosome;
	for (my $i=0;$i<@get_addChromosome;++$i)
	{
		push @temp_copy_chromosome,$get_addChromosome[$i];
	}
	return @temp_copy_chromosome;
}
##**end �ƻs ###

### ��t�G���I��t ###
sub crossover
{
	### �N�t�諸�V���馸�ǥ���########
	my @tempSeed1=();
	my @tempSeed2=();

	for(my $i=0;$i<$chromosome_count;++$i)
	{
		my $temp_ran=int (rand 2);
		if($temp_ran==0 && ($#tempSeed1+$#tempSeed2+1)<=$chromosome_count-1)
		{
			push @tempSeed1,$i;
		}
		elsif($temp_ran==1 && ($#tempSeed1+$#tempSeed2+1)<=$chromosome_count-1)
		{
			push @tempSeed2,$i;
		}
		else	#�ҥ~�B�z
		{
			print "XXXXXXXXXXXXXXXXXXXXXX $temp_ran XXXXXXXXXXXXXXXXX\n";
		}
	}
	push @RandSeed,@tempSeed1;
	push @RandSeed,@tempSeed2;

	#print @RandSeed;

	##########################

	my @crossover_chromosome1=();
	my @crossover_chromosome2=();
	my $crossRate=$crossover_rate;

	for(my $i=0;$i<$chromosome_count;$i=$i+2)
	{
		#�p�G��X�Ӫ�rand�Ƥ���ܲv�j�A����N���i���t�A�����N�V�����X��U�@�N
		my $this_chromosome_rand = rand(1);

		if ($this_chromosome_rand >$crossRate)
		{
			for(my $g=0;$g<$gene_count;++$g)
			{
				push @crossover_chromosome1,$last_chromosome[($gene_count*$RandSeed[$i])+$g];
				push @crossover_chromosome2,$last_chromosome[($gene_count*$RandSeed[$i+1])+$g];
				#print $last_chromosome[$gene_count*$RandSeed[$i]+$g]."\t";
				#print $last_chromosome[$gene_count*$RandSeed[$i+1]+$g]."\t";
				#print "\n";
			}
		}
		else
		{
			my $first_point=int(rand($gene_count)); #���I��t���Ĥ@���I�A�|����0~�p���]�ƪ��ü�
			my $second_point=int(rand($gene_count-$first_point))+$first_point; #���I��t���ĤG���I�A�|����0~�p��first_point���ü�
			#$chromosome_num=0;

			for(my $j=0;$j<$gene_count;++$j)
			{
				if($j>=$first_point && $j<=$second_point)	#������I�����A�Npush �O�H��]�A�_�h�Npush �ۤw��]
				{
					#$gene_count*$RandSeed[] �N��_�l��m�A+$chromosome_num �N��ӬV���骺�ĴX�Ӱ�]
					push @crossover_chromosome1,$last_chromosome[$gene_count*$RandSeed[$i+1]+$j];
					push @crossover_chromosome2,$last_chromosome[$gene_count*$RandSeed[$i]+$j];
					#print $last_chromosome[$gene_count*$RandSeed[$i+1]+$chromosome_num]."\t";
					#print $last_chromosome[$gene_count*$RandSeed[$i]+$chromosome_num]."\t";
				}
				else	#�L�Ĥ@��(�ۤv)
				{
					push @crossover_chromosome1,$last_chromosome[$gene_count*$RandSeed[$i]+$j];
					push @crossover_chromosome2,$last_chromosome[$gene_count*$RandSeed[$i+1]+$j];
					#print $last_chromosome[$gene_count*$RandSeed[$i]+$chromosome_num]."\t";
					#print $last_chromosome[$gene_count*$RandSeed[$i+1]+$chromosome_num]."\t";
				}
				#++$chromosome_num;
			}
			#print "$first_point  $second_point\n";
		}
	}
	@RandSeed=();
	my @AllCrossoverChromosome=();
	push @AllCrossoverChromosome,@crossover_chromosome1;
	push @AllCrossoverChromosome,@crossover_chromosome2;
	return @AllCrossoverChromosome;
}
##**end ��t ###

### ���� ###
sub mutation()
{
	my $AllGeneCount = $gene_count* $chromosome_count; 	#�`��]��
	my $TheMutationRate=$mutation_rate; 				#�]�w�����ܲv
	my $WantTo_MutationCount =$AllGeneCount*$TheMutationRate;
	my @temp_mut=@over_cross;
	$WantTo_MutationCount=int($WantTo_MutationCount+0.5);#�|�ˤ��J

	#�Y�`��]��*���ܲv �p�� 1���ܡA�N0.9�����v�i�����1�Ӱ�]�A0.1�����v���i�����
	if ($WantTo_MutationCount <=0)
	{
		if(rand(1)>0.9)
		{
			$WantTo_MutationCount=1;
		}
	}
	for($i=1;$i<=$WantTo_MutationCount;++$i)
	{
		my $chang_MatrixPosition= int(rand($AllGeneCount));
		$temp_mut[$chang_MatrixPosition]= sprintf "%.3f", rand(1);

		#print "XX$temp_mut[$chang_MatrixPosition].X$chang_MatrixPosition\n";
	}
	return @temp_mut;
}
##**end ���� ###

###���W�ơG�ϧ���ҥ[�_�Ӭ�100% (�Y��1) ###
sub normalization()
{
	my @temp_norm=@_;
	for(my $i=0;$i<$chromosome_count;++$i)
	{
		my $one_chromAll=0;
		for(my $j=0;$j<$gene_count;++$j)
		{
			$one_chromAll+=$temp_norm[$i*$gene_count+$j];
		}
		for(my $k=0;$k<$gene_count;++$k)
		{
			if($one_chromAll==0)	#�ҥ~�B�z
			{
			   print "=====================������0=====================";
			}
			$temp_norm[$i*$gene_count+$k] /= $one_chromAll;
			$temp_norm[$i*$gene_count+$k]= sprintf "%.3f",$temp_norm[$i*$gene_count+$k];
		}
		#my $gg=0;
		#for(my $m=0;$m<$gene_count;++$m)
		#{
		#	$gg+=$temp_norm[$i*$gene_count+$m];
		#}
		#print "$gg\n";
	}
	return @temp_norm;
}
##**���W��###

