import AppKit

let root = CommandLine.arguments.count > 1 ? CommandLine.arguments[1] : "."
let source = root + "/main-three-owl-step1a-scale-check-v4-luke-brows.png"
let output = root + "/main-three-owl-step1a-pixel-guide.png"
guard let base = NSImage(contentsOfFile: source) else { fatalError("missing source") }
let size = NSSize(width: 1536, height: 1024)
let image = NSImage(size: size)
image.lockFocus()
base.draw(in: NSRect(origin: .zero, size: size))

func y(_ top: CGFloat) -> CGFloat { 1024 - top }
func box(_ x: CGFloat, _ top: CGFloat, _ w: CGFloat, _ h: CGFloat) {
  let p = NSBezierPath(roundedRect: NSRect(x: x, y: y(top + h), width: w, height: h), xRadius: 8, yRadius: 8)
  NSColor(calibratedWhite: 0.995, alpha: 0.94).setFill(); p.fill()
  NSColor(hex: "DCD5D2").setStroke(); p.lineWidth = 1; p.stroke()
}
extension NSColor {
  convenience init(hex: String) {
    let v = Int(hex, radix: 16) ?? 0
    self.init(red: CGFloat((v >> 16) & 255)/255, green: CGFloat((v >> 8) & 255)/255, blue: CGFloat(v & 255)/255, alpha: 1)
  }
}
func text(_ s: String, _ x: CGFloat, _ top: CGFloat, _ size: CGFloat, bold: Bool = false, center: Bool = false) {
  let style = NSMutableParagraphStyle(); style.alignment = center ? .center : .left
  let attrs: [NSAttributedString.Key:Any] = [.font: bold ? NSFont.boldSystemFont(ofSize: size) : NSFont.systemFont(ofSize: size), .foregroundColor:NSColor(hex:"291712"), .paragraphStyle:style]
  s.draw(in: NSRect(x:x, y:y(top+size+5), width:center ? 1000 : 390, height:size+10), withAttributes:attrs)
}
func line(_ x1: CGFloat,_ t1: CGFloat,_ x2: CGFloat,_ t2: CGFloat,_ color: NSColor = NSColor(hex:"7D2741"), dashed: Bool = false) {
  let p=NSBezierPath(); p.move(to:NSPoint(x:x1,y:y(t1))); p.line(to:NSPoint(x:x2,y:y(t2))); p.lineWidth=2
  if dashed { var d:[CGFloat]=[8,8]; p.setLineDash(&d,count:2,phase:0) }
  color.setStroke(); p.stroke()
}
func vdim(_ x:CGFloat,_ top:CGFloat,_ bottom:CGFloat){ line(x,top,x,bottom); line(x-7,top+8,x,top); line(x+7,top+8,x,top); line(x-7,bottom-8,x,bottom); line(x+7,bottom-8,x,bottom) }
func hdim(_ left:CGFloat,_ right:CGFloat,_ top:CGFloat){ line(left,top,right,top); line(left+8,top-7,left,top); line(left+8,top+7,left,top); line(right-8,top-7,right,top); line(right-8,top+7,right,top) }

box(268,30,1000,108); text("STEP 2 — PIXEL MEASUREMENT",268,52,40,bold:true,center:true); text("1536×1024 master canvas · front geometry locked 1:1 · no accessories",268,103,17,center:true)
line(60,844,1476,844,NSColor(hex:"8D8380"),dashed:true)
let specs:[(CGFloat,String,String,String,CGFloat,CGFloat,CGFloat,CGFloat)] = [
 (78,"MIMO","FULL 340 · HEAD 122×133","EYE 10×20 · CENTERS 55 · BEAK 25×24",118,504,176,298),
 (437,"GEN","FULL 488 · HEAD 180×160","EYE 15×27 · CENTERS 69 · NOSE 13×9",438,356,498,678),
 (790,"LUKE","FULL 440 · HEAD 142×184 · TORSO W 219","EYE 16×18 · CENTERS 69 · NOSE 30×20",772,404,854,996),
 (1153,"OWL","FULL 397 · BODY W 218 · FACE 173×185","EYE 24×42 · CENTERS 70 · BEAK 25×29",1150,447,1192,1410)
]
for (x,n,a,b,vx,vt,hl,hr) in specs { box(x,282,x == 790 ? 356 : (x == 1153 ? 322 : 330),108); text(n,x+18,296,27,bold:true); text(a,x+18,332,x == 790 ? 15 : 17); text(b,x+18,360,15); vdim(vx,vt,844); hdim(hl,hr,x == 78 ? 480 : (x == 1153 ? 446 : (x == 790 ? 400 : 401))) }
box(300,902,936,78); text("LOCK ORDER: full height → head box → torso width → eye centers → eye size → nose/beak → mouth",268,916,17,center:true); text("Never redraw or independently rescale the head, face, torso, or tail in a pose sheet.",268,946,15,center:true)

image.unlockFocus()
guard let tiff=image.tiffRepresentation, let rep=NSBitmapImageRep(data:tiff), let png=rep.representation(using:.png,properties:[:]) else { fatalError("render failed") }
try png.write(to:URL(fileURLWithPath:output))
