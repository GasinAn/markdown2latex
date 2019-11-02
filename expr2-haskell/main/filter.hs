import Text.Pandoc
import Text.Pandoc.Walk (walk)
import Text.Pandoc.JSON

-- [Header 1 ("title",[],[]) [Str "Title"]
-- ,Para [Image ("",[],[]) [] ("img.png","")]
-- ,BlockQuote
--  [Para [Str "key:",Space,Str "value",SoftBreak,Str "k2",Space,Str ":",Space,Str "val2"]]]

maniImage :: Block -> Block
maniImage (Header n _ xs) | n >= 2 = Para [Emph xs]
maniImage x = x

main :: IO ()
main = toJSONFilter maniImage