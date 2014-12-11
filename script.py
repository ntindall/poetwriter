import subprocess
print 'Whitman n=1...'
subprocess.Popen('python generator.py -n 1 -l 2 -b 5 -r 5 -f "corpora/whitman.txt" -o 20 -t eight > new_output/whitman-n1.txt', shell=True)
print 'Whitman n=2...'
subprocess.Popen('python generator.py -n 2 -l 2 -b 5 -r 5 -f "corpora/whitman.txt" -o 20 -t eight > new_output/whitman-n2.txt', shell=True)
print 'Whitman n=3...'
subprocess.Popen('python generator.py -n 3 -l 2 -b 5 -r 5 -f "corpora/whitman.txt" -t eight -o 20 > new_output/whitman-n3.txt', shell=True)
print 'Whitman b=10...'
subprocess.Popen('python generator.py -n 3 -l 2 -b 10 -f "corpora/whitman.txt" -t eight -o 20 > new_output/whitman-b10.txt', shell=True)
print 'Shakespeare b=10...'
subprocess.Popen('python generator.py -n 3 -l 2 -b 10 -f "corpora/shakespeare.txt" -t eight -o 20 > new_output/shakes-b10.txt', shell=True)
print 'Shakespeare n=1...'
subprocess.Popen('python generator.py -n 1 -t eight -l 2 -b 5 -r 5 -f "corpora/shakespeare.txt" -o 20 > new_output/shakes-n1.txt', shell=True)
print 'Shakespeare n=2...'
subprocess.Popen('python generator.py -n 2 -l 2 -b 5 -r 5 -f "corpora/shakespeare.txt" -t eight -o 20 > new_output/shakes-n2.txt', shell=True)
print 'Shakespeare n=3...'
subprocess.Popen('python generator.py -n 3 -l 2 -b 5 -r 5 -f "corpora/shakespeare.txt" -t eight -o 20 > new_output/shakes-n3.txt', shell=True)
print 'Eliot n=1...'
subprocess.Popen('python generator.py -n 1 -t eight -l 2 -b 5 -r 5 -f "corpora/eliot.txt" -o 20 > new_output/eliot-n1.txt', shell=True)
print 'Eliot n=2...'
subprocess.Popen('python generator.py -n 2 -l 2 -b 5 -r 5 -f "corpora/eliot.txt" -t eight -o 20 > new_output/eliot-n2.txt', shell=True)
print 'Eliot n=3...'
subprocess.Popen('python generator.py -n 3 -l 2 -b 5 -r 5 -f "corpora/eliot.txt" -t eight -o 20 > new_output/eliot-n3.txt', shell=True)


