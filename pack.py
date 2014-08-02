#----------------------------------introduction---------------------------------#
'''the aim of this tool is to ergolist the asset path
and create a "uiAsset.as" file to map the bitmaps to
"Embed" class

how to use this bat tool:
1.place this script file in the asset directory,and make sure
that all the bitmap file was in the current path or subpath

2.if you wanna provide a bitmap's 9scaleGrid info,config the
relative info into a file(default named: 9.txt) under the same
directory path of the bitmap,and info goes like this:
["bg0","scaleGridTop=55,scaleGridLeft=55,scaleGridBottom=64,scaleGridRight=65"]
or:
["all_same","scaleGridTop=55,scaleGridLeft=55,scaleGridBottom=64,scaleGridRight=65"]

3.run the script,then check if a codefile is generated correctly.
'''
#-----------------------------------global config infos-------------------------#
#bitmaps extention
bmpx = ['bmp','jpg','png']

#config scale info file name
cfg = '9.txt'
'''in current directory,if all the bitmap file use the same config info,
use the follow tag str as the info key,this model was usually take to cfg a button's asset
eg:  ["all_same","scaleGridTop=55,scaleGridLeft=55,scaleGridBottom=64,scaleGridRight=65"]'''
cfg_info_ally_tag = "all_same"

#create code file
codefile = './Assets.as'
code_indent = '\t\t'

#whether show the "Done" word when progress finish,if not, the progress will
#exit automaticly,default is not
show_done_info = False#True


#-----------------------------------functions definition---------------------#

def ergo(pname):
    '''ergolist the given path
and list the bitmap file name into a string
'''
    import os
    import glob
    #first,pname should be a directory:
    if os.path.isfile(pname):
        return
    os.chdir(pname)
    
    #first check if exits cfg file 
    #if so,read info from it
    cfginfo = []
    if os.path.exists(cfg):
        
        cfgfile = open(os.path.join(pname,cfg))
        for line in cfgfile:
            name, info = eval(line)
            ele = {"name":name,"info":info}
            cfginfo.append(ele)
            #print ele

    #parse dir and file:
    flist = glob.glob("*")
    for f in flist:
        
        pathf = os.path.join(pname,f)
        #sub directory:
        if os.path.isdir(pathf):
            ergo(pathf)
        #files to deal with:
        elif pathf.split(".")[-1:][0] in bmpx:
            createEmbedCode(pathf,cfginfo)
            #print pathf
            


def createEmbedCode(pathf,cfginfo):
    ''' use file's path name and the configinfo,
create Embed code and cache'''

    import os
    pathSplit = pathf.split(os.sep)
    fname = os.path.basename(pathf).split(".")[0]
   
    cfgStr = ''
    if len(cfginfo)>0:
        for info in cfginfo:
            if info["name"] == fname or info["name"] == cfg_info_ally_tag:
                cfgStr = ','+info["info"]
                break
    

    idx = pathSplit.index(asset_root_name)+1
    ast_cls_name = '_'.join(pathSplit[idx:-1])+ '_' + fname
    ast_file_path = os.path.relpath(pathf,asset_root)

    
    code = code_indent + '[Embed(source="' \
           + './'+'/'.join(ast_file_path.split('\\')) \
           +'"'+ cfgStr + ')]\n' + code_indent \
           + 'public static const ' + ast_cls_name + ':Class;\n'
    codefl.write(code)

    asset_array.append( repr(ast_cls_name) )
    
    

#-------------------------------enter progress---------------------------------#

if __name__ == "__main__":
    import os
    
    asset_root = os.getcwd()
    asset_root_name = os.path.basename(asset_root)

    '''script file head:'''
    file_head = 'package ' + asset_root_name+'\n\
{\n\t/**\n\t* @author leui\n\t*/\n\tpublic class Assets\n\t{\n'
    '''script file tail'''
    file_tail = code_indent+ 'public function Assets(){}\n\t}\n}\n'

    '''open code file '''
    codefl = open(codefile,'w')
    '''write head which include package info of the as file'''
    codefl.write(file_head)
    
    '''init the asset_array,
    which will later be used to cache all the bitmap file's names'''
    asset_array = []
    '''run the ergolist function and generate assets' embed code'''
    ergo(asset_root)
    '''fix up the asset_array into a code str'''
    asset_dic_code = code_indent + 'public static const assetCls:Array = ['\
                     + ','.join(asset_array) + '];\n'
    
    codefl.write(asset_dic_code)
    codefl.write(file_tail)

    '''finish progress'''
    if show_done_info:
        input("Done!\npress Enter key to exit")
    exit()


