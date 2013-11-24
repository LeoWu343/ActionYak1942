package main
import (
    "fmt"
    "image"
    "os"
    "flag"
    "image/png"
    "image/color"
    _ "image/gif"
    _ "image/jpeg"
)


var MSGSIGNATURE="__%%__$$__"
var KEY_DELIMETER="|||"

//Struct Definitions
type Args struct{
    decode bool
    encode bool
    fileName string
    message string
    outFileName string
    key string
}

//Pipeline
func encode(img image.Image, message string, key string)(image.Image){
    message = MSGSIGNATURE + key + KEY_DELIMETER + message + "\u0000"
    var bounds = img.Bounds()
    var width, height = bounds.Max.X, bounds.Max.Y
    var size = width*height
    var out = image.NewRGBA(image.Rect(0,0,width,height))
    //Pointless Comment
    var code = make([]bool,len(message)*8)
    for i := 0; i < len(message); i++{
        var char = message[i]
        for j:=7; j >= 0; j--{
            code[8*i+j]=(char >> uint8(j))&1==1
        }
    }
    var i int
    for i = 0; i < len(code); i++{
        var x = (i%size)%width
        var y = (i%size)/width
        var k = i/size
        if k >= 3{
            die([]string{"Insufficient space in image for message"})
        }
        var r, g, b, a = img.At(x,y).RGBA()
        var newColor color.RGBA
        switch k{
        case 0:
            newColor=color.RGBA{getCodeVal(r,code[i]),uint8(g>>8),uint8(b>>8),uint8(a>>8)}
        case 1:
            newColor=color.RGBA{uint8(r>>8),getCodeVal(g,code[i]),uint8(b>>8),uint8(a>>8)}
        case 2:
            newColor=color.RGBA{uint8(r>>8),uint8(g>>8),getCodeVal(b,code[i]),uint8(a>>8)}
        default:
            die([]string{"Something that should not have happened happened"})
        }
        out.Set(x,y,newColor)
    }
    for ;i < size;i++{
        var x = (i%size)%width
        var y = (i%size)/width
        out.Set(x,y,img.At(x,y))
    }
    return out
}

func decode(img image.Image)(string){
    var bounds = img.Bounds()
    var width, height = bounds.Max.X, bounds.Max.Y
    var size = width*height
    //Get raw data
    var raw = make([]bool,size*3)
    for k:=0;k<3;k++{
        for y:=0;y<height;y++{
            for x:=0;x<width;x++{
                var r32, g32, b32, _ = img.At(x,y).RGBA()
                var r=uint8(r32>>8)
                var g=uint8(g32>>8)
                var b=uint8(b32>>8)
                switch k{
                case 0:
                    raw[k*size+y*width+x]=(r%2!=0)
                case 1:
                    raw[k*size+y*width+x]=(g%2!=0)
                case 2:
                    raw[k*size+y*width+x]=(b%2!=0)
                default:
                    die([]string{"Something that should not have happened happened"})
                }
            }
        }
    }

    //Break data into bytes
    /*

    for i in range(8):
        if x[i]==1:
            k+=1<<(i)
        print(bin(k))

    */
    var bytes = make([]byte,len(raw)/8)
    var b byte
    for i:=0; i < len(raw)/8-1; i++{
        b = 0
        for j := 0; j < 8; j++{
            if raw[8*i+j]{
                b+=(1<<uint8(j))
            }
        }
        bytes[i] = b
        if b==0{
            bytes=bytes[:i+1]
            break;
        }
    }
    return string(bytes)
}

//Main
func main(){
    var args = getArgs()
    var img = loadImg(args.fileName)
    if args.encode{
        writeImg(encode(img,args.message, args.key),args.outFileName)
    }else if args.decode{
        fmt.Println(decode(img))
    }
}

//Helper functions
func getArgs()(Args){
    var decode=flag.Bool("d", false, "Set script to decode message")
    var encode=flag.Bool("e", false, "Set script to encode message")
    flag.Parse()

    if *decode && *encode{
        die([]string{"Cannot encode and decode at the same time"})
    }
    if !*decode && !*encode{
        die([]string{"Nothing to do! (set flag -d to decode or -e to encode)"})
    }

    if (*encode && flag.NArg()<3) || (*decode && flag.NArg()<1){
        die([]string{"Missing Filename and/or message"})
    }

    var fileName = flag.Arg(0)
    var message = ""
    var outFileName = ""
    var key = ""
    if *encode{
        message = flag.Arg(2)
        outFileName = flag.Arg(1)
        key = flag.Arg(3)
    }
    return Args{*decode,*encode,fileName,message,outFileName, key}
}
func loadImg(path string)(image.Image){
    var file, openerr = os.Open(path)
    defer file.Close()
    if openerr!=nil{
        die([]string{"Failed to open file at " + path})
    }
    var img, _, decodeerr = image.Decode(file)
    if decodeerr!=nil{
        die([]string{"File at " + path + " is not a recognized image format"})
    }
    return img
}
func writeImg(img image.Image, path string){
    var file, _ =  os.Create(path)
    defer file.Close()
    png.Encode(file,img)
}
func getCodeVal(val uint32, odd bool)(uint8){
    if odd{
        return uint8(makeOdd(val))
    }else{
        return uint8(makeEven(val))
    }
}
func makeOdd(val uint32)(uint32){
    if (val%2==1){
        return val
    }else{
        return val+1
    }
}
func makeEven(val uint32)(uint32){
    if (val%2==0){
        return val
    }else{
        if val!=255{
            return val+1
        }else{
            return val-1
        }
    }
}
func die(errors []string){
    if len(errors)>0{
        var errormsg = "Script has terminated because of the following errors:\n"
        for i:=0; i<len(errors); i++{
            errormsg += "\t"+errors[i]+"\n"
        }
        fmt.Fprint(os.Stderr,errormsg)
    }
    os.Exit(1)
}
