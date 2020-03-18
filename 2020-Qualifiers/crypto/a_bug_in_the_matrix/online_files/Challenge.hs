import Control.Monad
import System.Environment
import System.Random
import Numeric
import Data.Text.Internal.Read
import Data.Char
import Data.Array.IO
import Data.Bits
import Data.List

type Bit = Bool
type Permutation = [Int]
type BitArray = [Bit]
-- Each round key contains an array and a permutation.
data RoundKey = RoundKey BitArray Permutation
-- A key is a list of round keys. Each round has a different round key
type Key = [RoundKey]
type Hex = String

zeroBit :: Bit
zeroBit = False

blockSize = 512
keySize = div blockSize 2
rounds = 256

main = initKey >>= start

-- Generate a random key
initKey :: IO Key
initKey = sequence $ replicate rounds generateRoundKey
    where
        generateRoundKey = do
            perm <- shuffle [0..keySize-1]
            key <- replicateM keySize randomIO
            return $ RoundKey key perm

-- Print the encrypted flag and show the encryption prompt
start :: Key -> IO b
start key =
    putStrLn "The encrypted flag is:"
    >> getEnv "FLAG"
    >>= putStrLn . encryptString key
    >> encryptionPrompt key

-- Show the encryption prompt in a loop
-- Each iterations asks for a hex string of input, encrypts it, and sends it back
encryptionPrompt :: Key -> IO b
encryptionPrompt key =
    putStrLn "Enter hexstring to encrypt." 
    >> getLine
    >>= putStrLn . encryptHex key
    >> encryptionPrompt key

-- Convert hex data to bit array, encrypt it and convert back to hex data
encryptHex :: Key -> Hex -> Hex
encryptHex key = bitArrayToHex . encryptBitArray key . hexToBitArray

-- Convert string to bit array, encrypt it and convert back to hex
encryptString :: Key -> String -> Hex
encryptString key = bitArrayToHex . encryptBitArray key . stringToBitArray

-- Left pad the bit array to a multiple of the blocksize, split it in blocks of the correct size, and encrypt each block
encryptBitArray :: Key -> BitArray -> BitArray
encryptBitArray key = (encryptBlock key =<<) . chunksOf blockSize . leftPad blockSize zeroBit

-- Encrypt one block with a Feistel scheme (https://en.wikipedia.org/wiki/Feistel_cipher)
encryptBlock :: Key -> BitArray -> BitArray
encryptBlock = flip . foldl $ flip feistelRound

-- Apply one Feistel round
feistelRound :: RoundKey -> BitArray -> BitArray
feistelRound key plain = 
        let (left, right) = splitAt keySize plain
        in xorArray right (roundFunction key left) ++ left

-- Round function first applies a permutation and then xor's with the key
roundFunction :: RoundKey -> BitArray -> BitArray
roundFunction (RoundKey xorKey permutation) = xorArray xorKey . permute permutation 

-- Helper functions
leftPad :: Int -> a -> [a] -> [a]
leftPad l filler xs 
    | (length(xs) `mod` l) /= 0 = leftPad l filler (filler : xs)
    | otherwise = xs

bitArrayToHex :: BitArray -> Hex 
bitArrayToHex = (asHex . bitArrayToInt =<<) . chunksOf 4
    where
        asHex h = showHex h ""
        bitArrayToInt [] = 0
        bitArrayToInt (x:xs) = 2 ^ (length xs) * bitToInt x + bitArrayToInt xs
        bitToInt True = 1
        bitToInt _ = 0

hexToBitArray :: Hex -> BitArray
hexToBitArray = (>>= leftPad 4 zeroBit . intToBitArray . hexDigitToInt) . trim

stringToBitArray :: Hex -> BitArray
stringToBitArray = (>>= leftPad 8 zeroBit . intToBitArray . ord) . trim

intToBitArray :: Int -> BitArray
intToBitArray 0 = [zeroBit]
intToBitArray x = intToBitArray' x
    where
        intToBitArray' 0 = []
        intToBitArray' x = intToBitArray' (div x 2) ++ [ 1 == mod x 2 ]

xorArray :: BitArray -> BitArray -> BitArray
xorArray [] [] = []
xorArray (x:xs) (y:ys) = (xor x y) : xorArray xs ys

chunksOf :: Int -> [a] -> [[a]]
chunksOf _ [] = []
chunksOf n xs =
    let (ys, zs) = splitAt n xs
    in  ys : chunksOf n zs

-- https://wiki.haskell.org/Random_shuffle
-- | Randomly shuffle a list
--   /O(N)/
shuffle :: [a] -> IO [a]
shuffle xs = do
        ar <- newArray n xs
        forM [1..n] $ \i -> do
            j <- randomRIO (i,n)
            vi <- readArray ar i
            vj <- readArray ar j
            writeArray ar j vi
            return vj
  where
    n = length xs
    newArray :: Int -> [a] -> IO (IOArray Int a)
    newArray n xs =  newListArray (1,n) xs

permute :: Permutation -> [a] -> [a]
permute [] _ = []
permute (x:xs) list = (list !! x) : permute xs list

trim = dropWhileEnd isSpace . dropWhile isSpace
