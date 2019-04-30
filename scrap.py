import os
import re, subprocess
#import pdf_to_text
# regex to find txt file
re1='.*?'	# Non-greedy match on filler
re2='(\\.)'	# Any Single Character 1
re3='(txt)'	# Word 1
rg = re.compile(re1 + re2 + re3, re.IGNORECASE | re.DOTALL)
content =[]
# regex for email
#email_re1='\S+@\S+'
email_re1='[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,4}'
email_rg = re.compile(email_re1,re.IGNORECASE|re.DOTALL)

# names to be removed
name_list = [ 'Anne Roth','Brendan Weber','Emily Foley','Allison Wolf','Meredith McCarthy','Greg Hartman',"Todd O'Brien",
             'Brad Snyder','Seth Gallagher','Jill Becker','Jamal Jefferson','Darnell Washington','Latoya Banks',
             'Lakisha Mosley','Keisha Jackson','Tanisha Charles','Tyrone Dorsey','Tamika Rivers','Tremayne Booker',
             'Jermaine Gaines']

for dir in os.listdir('.'):
    if dir == 'Craigslist':
        for subdir in os.listdir(dir):
            if not subdir.startswith('.') and os.path.isdir(os.path.join(dir, subdir)):
                for files in os.listdir(dir+'/'+subdir):
                    if '.pdf' in files.lower():
                        text_file = open(dir+'/'+subdir+'/'+files.split('.')[0]+'.txt','w')
                        print ('-----------------',files)
                        files_mutate = files
                        if ' ' in files:
                            files_mutate = files.replace(' ', '\ ')
                        print ('calling ','python2.7 pdf_to_text.py ' + dir+'/'+subdir+'/'+files_mutate)
                        output = subprocess.check_output('python2.7 pdf_to_text.py ' + dir+'/'+subdir+'/'+files_mutate, shell=True)
                        lines = str(output, 'utf-8')
                        line = ''
                        for name in name_list:
                            name_split = name.split(' ')
                            if name_split[0].lower() in lines.lower() or name_split[1].lower() in lines.lower():
                                line = lines.replace(name_split[0], '###').replace(name_split[1], '###')
                        # remove email
                        email_m = email_rg.search(lines)
                        if email_m:
                            line = line.replace(email_m.group(), '###@##.com')
                        lines = line + '\n'
                        # create new files
                        if not os.path.exists(os.path.join('./updated_craiglist', subdir)):
                            os.makedirs(os.path.join('./updated_craiglist', subdir))
                        with open(os.path.join('./updated_craiglist', subdir,files.split('.')[0]+'.txt'), 'w', errors='ignore')as f:
                            f.writelines(lines)






