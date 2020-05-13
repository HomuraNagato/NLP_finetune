


if __name__ == '__main__':

    f = open('/mnt/c/Users/Nagato/Documents/hacker_data/congress_text/hein-bound/filtered_speakers_111.txt', encoding='latin')

    f_0 = open('/mnt/c/Users/Nagato/Documents/hacker_data/congress_text/hein-bound/filtered_111120961.txt', 'w+', encoding='latin')
    f_1 = open('/mnt/c/Users/Nagato/Documents/hacker_data/congress_text/hein-bound/filtered_111118321.txt', 'w+', encoding='latin')
    f_2 = open('/mnt/c/Users/Nagato/Documents/hacker_data/congress_text/hein-bound/filtered_111116550.txt', 'w+', encoding='latin')
    f_3 = open('/mnt/c/Users/Nagato/Documents/hacker_data/congress_text/hein-bound/filtered_111120391.txt', 'w+', encoding='latin')

    auth = [0, 0, 0, 0]
    for line in f:
        if '111120961' in line:
            auth[0] += 1
            f_0.write(line)
        elif '111118321' in line:
            auth[1] += 1
            f_1.write(line)
        elif '111116550' in line:
            auth[2] += 1
            f_2.write(line)
        elif '111120391' in line:
            auth[3] += 1
            f_3.write(line)
    print(auth, sum(auth))
    f.close()
    f_0.close()
    f_1.close()
    f_2.close()
    f_3.close()



