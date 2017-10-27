# 字符串之字形序列的转换

```cpp
class Solution {
public:
    string convert(string s, int numRows) {
        if (numRows == 1)
            return s;
            
        int size = s.size();
        string res;
        int max_jump = 2*numRows-2;
        
        for (int line=0; line < numRows; line++) {
            int r = 2*line;
            if (line == 0 || line == numRows-1) {
                int index = line;
                int jump = max_jump;
                while(index < size) {
                    res += s.at(index);
                    index+=jump;
                }
                //std::cout << "line:" << line << "result:" << res << std::endl;
            } else {
                int index = line;
                while(index < size) {
                    //std::cout << "jump=" << r << "index:" << index << std::endl;
                    res+=s.at(index);
                    r = max_jump - r;
                    index+=r;
                }
            }
        }
        //std::cout << res << std::endl;
        return res;
    }
};
```