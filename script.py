import subprocess
print 'Whitman n=1...'
subprocess.Popen('python generator.py -n 1 -l 2 -b 3 -r 3 -f corpora/whitman.txt -o 20 -t eight > output/whitman-n1.txt', shell=True)
print 'Whitman n=2...'
subprocess.Popen('python generator.py -n 2 -l 2 -b 3 -r 3 -f corpora/whitman.txt -o 20 -t eight > output/whitman-n2.txt', shell=True)
print 'Whitman n=3...'
subprocess.Popen('python generator.py -n 3 -l 2 -b 3 -r 3 -f corpora/whitman.txt -t eight -o 20 > output/whitman-n3.txt', shell=True)
print 'Whitman b=20...'
subprocess.Popen('python generator.py -n 2 -l 2 -b 20 -f corpora/whitman.txt -t eight -o 20 > output/whitman-b20.txt', shell=True)
print 'Shakespeare n=1...'
subprocess.Popen('python generator.py -n 1 -l 2 -b 3 -r 3 -f corpora/shakespeare.txt -o 20 -t eight > output/shakes-n1.txt', shell=True)
print 'Shakespeare n=2...'
subprocess.Popen('python generator.py -n 2 -l 2 -b 3 -r 3 -f corpora/shakespeare.txt -t eight -o 20 > output/shakes-n2.txt', shell=True)
print 'Shakespeare n=3...'
subprocess.Popen('python generator.py -n 3 -l 2 -b 3 -r 3 -f corpora/shakespeare.txt -t eight -o 20 > output/shakes-n3.txt', shell=True)
print 'Eliot n=1...'
subprocess.Popen('python generator.py -n 1 -t eight -l 2 -b 3 -r 3 -f corpora/eliot.txt -o 20 > output/eliot-n1.txt', shell=True)
print 'Eliot n=2...'
subprocess.Popen('python generator.py -n 2 -l 2 -b 3 -r 3 -f corpora/eliot.txt -t eight -o 20 > output/eliot-n2.txt', shell=True)
print 'Eliot n=3...'
subprocess.Popen('python generator.py -n 3 -l 2 -b 3 -r 3 -f corpora/eliot.txt -t eight -o 20 > output/eliot-n3.txt', shell=True)


