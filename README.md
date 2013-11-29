# pyles (what the hell?)

So, since my day job consists of being in the ruby on rails eco-system, I've come to experience the value of opinions in the toolset.

This library is my attempt in my spare time to get some of the same kinds of things I appreciate in rails made available to me for the various python/pyramid projects I may work on. 

For example, my favorite web framework(pyramid) offers no opinion on how to organize your project. This is a good thing. BUT, I have an opinion on how to organize things, and it deviates a bit from the scaffolds offered. So I would like a way to enforce my opinions on project organization.

An ideal use case for me would be something like the following......


``` shell

$ pyles create project new_project -p /usr/bin/python3


creating virtualenv for new_project at ./new_project/.env
........................................................done

download buildout bootstrap.py............


create ./new_project/buildout.cfg
create ./new_project/versions.cfg


create project skeleton at ./new_project/src/new_project

running buildout

./new_project/.env/bin/python bootstrap.py
./new_project/bin/buildout -c buildout.cfg

```

So I can get that cooking relatively easily. But what I would also like

``` shell

./new_project/src/new_project $ pyles create view profile

creating view at ./new_project/views/profile.py
creating test at ./test/views/test_profile.py
     
```

Many of these things can be driven by templates a la paste, pcreate, cookiecutter etc.....

paste doesn't work with python 3

pcreate is tied to pyramid and I wanted something more general or at least am wondering if something more general would appeal to me or others.

cookiecutter is fine, I just wanted to see if I could do this. 

This is also an excuse to play with python 3 so I don't plan on purposely supporting python 2.x