A bunch of scripts for benchmarking
[RSqueak](https://github.com/HPI-SWA-Lab/RSqueak) vs
[Cog/Spur](http://www.mirandabanda.org/files/Cog/VM/latest/) and posting the
results to our
[Codespeed](https://www.hpi.uni-potsdam.de/hirschfeld/codespeed/). Very specific
to RSqueak. Probably not useful for re-use.

Note: how to get a system+vm version string:
```smalltalk
FileStream stdout
    cr;
    nextPutAll: 'VMcomboVersion: ';
    nextPutAll: 'img';
    nextPutAll: SystemVersion current highestUpdate printString.
(Smalltalk vm interpreterClass includesSubString: 'rsqueak')
    ifTrue: [
        FileStream stdout nextPutAll: 'vm'.
        (RxMatcher forString: ' [0-9a-f]+ ')
            matchesIn: Smalltalk vm vmVersion
            do: [:m | FileStream stdout nextPutAll: m withBlanksTrimmed].
        FileStream stdout
            nextPutAll: 'sim';
            nextPutAll: (MCPackage named: 'VMMaker') workingCopy
                              currentVersionInfo versionNumber printString]
    ifFalse: [
        FileStream stdout nextPutAll: 'vm'.
        (RxMatcher forString: '[0-9]+')
            matchesIn: Smalltalk vm vmVersion
            do: [:m | FileStream stdout nextPutAll: m].
        FileStream stdout nextPutAll: 'svn'.
        (RxMatcher forString: 'r[0-9]+')
            matchesIn: Smalltalk vm platformSourceVersion
            do: [:m | FileStream stdout nextPutAll: m]].
```
