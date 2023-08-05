// generic useful stuff for any C++ program

#ifndef RECRYPTO_TOOLS_H
#define RECRYPTO_TOOLS_H

#include <cstdlib>
#include <cstring>

#ifdef NULL
#undef NULL
#endif
#define NULL 0

typedef unsigned char uchar;
typedef unsigned short ushort;
typedef unsigned int uint;
typedef unsigned long ulong;
typedef signed long long int llong;
typedef unsigned long long int ullong;

#ifdef _DEBUG
#define ASSERT(c) assert(c)
#else
#define ASSERT(c) if(c) {}
#endif

inline void *operator new(size_t, void *p) { return p; }
inline void *operator new[](size_t, void *p) { return p; }
inline void operator delete(void *, void *) {}
inline void operator delete[](void *, void *) {}

#ifdef swap
#undef swap
#endif
template<class T>
static inline void swap(T &a, T &b)
{
    T t = a;
    a = b;
    b = t;
}
#ifdef max
#undef max
#endif
#ifdef min
#undef min
#endif
template<class T>
static inline T max(T a, T b)
{
    return a > b ? a : b;
}
template<class T>
static inline T min(T a, T b)
{
    return a < b ? a : b;
}
template<class T, class U>
static inline T clamp(T a, U b, U c)
{
    return max(T(b), min(a, T(c)));
}

#define loop(v,m) for(int v = 0; v < int(m); ++v)
#define loopi(m) loop(i,m)
#define loopj(m) loop(j,m)
#define loopk(m) loop(k,m)
#define loopl(m) loop(l,m)
#define looprev(v,m) for(int v = int(m); --v >= 0;)
#define loopirev(m) looprev(i,m)
#define loopjrev(m) looprev(j,m)
#define loopkrev(m) looprev(k,m)
#define looplrev(m) looprev(l,m)

#ifdef _MSC_VER
#pragma warning (3: 4189)       // local variable is initialized but not referenced
#pragma warning (disable: 4244) // conversion from 'int' to 'float', possible loss of data
#pragma warning (disable: 4267) // conversion from 'size_t' to 'int', possible loss of data
#pragma warning (disable: 4355) // 'this' : used in base member initializer list
#pragma warning (disable: 4800) // forcing value to bool 'true' or 'false' (performance warning)
#pragma warning (disable: 4996) // 'strncpy' was declared deprecated
#include <direct.h>
#endif

#define loopv(v)    for(int i = 0; i<(v).length(); i++)
#define loopvj(v)   for(int j = 0; j<(v).length(); j++)
#define loopvk(v)   for(int k = 0; k<(v).length(); k++)
#define loopvrev(v) for(int i = (v).length()-1; i>=0; i--)
#define loopvjrev(v) for(int j = (v).length()-1; j>=0; j--)
#define loopvkrev(v) for(int k = (v).length()-1; k>=0; k--)

template <class T>
struct databuf
{
    enum
    {
        OVERREAD  = 1<<0,
        OVERWROTE = 1<<1
    };

    T *buf;
    int len, maxlen;
    uchar flags;

    databuf() : buf(NULL), len(0), maxlen(0), flags(0) {}

    template<class U>
    databuf(T *buf, U maxlen) : buf(buf), len(0), maxlen((int)maxlen), flags(0) {}

    void reset()
    {
        len = 0;
        flags = 0;
    }

    void reset(T *buf_, int maxlen_)
    {
        reset();
        buf = buf_;
        maxlen = maxlen_;
    }

    const T &get()
    {
        static T overreadval = 0;
        if(len<maxlen) return buf[len++];
        flags |= OVERREAD;
        return overreadval;
    }

    databuf subbuf(int sz)
    {
        sz = clamp(sz, 0, maxlen-len);
        len += sz;
        return databuf(&buf[len-sz], sz);
    }

    T *pad(int numvals)
    {
        T *vals = &buf[len];
        len += min(numvals, maxlen-len);
        return vals;
    }

    void put(const T &val)
    {
        if(len<maxlen) buf[len++] = val;
        else flags |= OVERWROTE;
    }

    void put(const T *vals, int numvals)
    {
        if(maxlen-len<numvals) flags |= OVERWROTE;
        memcpy(&buf[len], (const void *)vals, min(maxlen-len, numvals)*sizeof(T));
        len += min(maxlen-len, numvals);
    }

    int get(T *vals, int numvals)
    {
        int read = min(maxlen-len, numvals);
        if(read<numvals) flags |= OVERREAD;
        memcpy(vals, (void *)&buf[len], read*sizeof(T));
        len += read;
        return read;
    }

    void offset(int n)
    {
        n = min(n, maxlen);
        buf += n;
        maxlen -= n;
        len = max(len-n, 0);
    }

    T *getbuf() const { return buf; }
    bool empty() const { return len==0; }
    int length() const { return len; }
    int remaining() const { return maxlen-len; }
    bool overread() const { return (flags&OVERREAD)!=0; }
    bool overwrote() const { return (flags&OVERWROTE)!=0; }

    bool check(int n) { return remaining() >= n; }

    void forceoverread()
    {
        len = maxlen;
        flags |= OVERREAD;
    }
};

typedef databuf<char> charbuf;
typedef databuf<uchar> ucharbuf;

template<class T> struct isclass
{
    template<class C> static char test(void (C::*)(void));
    template<class C> static int test(...);
    enum { yes = sizeof(test<T>(0)) == 1 ? 1 : 0, no = yes^1 };
};

template <class T> struct vector
{
    static const int MINSIZE = 8;

    T *buf;
    int alen, ulen;

    vector() : buf(NULL), alen(0), ulen(0)
    {
    }

    vector(const vector &v) : buf(NULL), alen(0), ulen(0)
    {
        *this = v;
    }

    ~vector() { shrink(0); if(buf) delete[] (uchar *)buf; }

    vector<T> &operator=(const vector<T> &v)
    {
        shrink(0);
        if(v.length() > alen) growbuf(v.length());
        loopv(v) add(v[i]);
        return *this;
    }

    T &add(const T &x)
    {
        if(ulen==alen) growbuf(ulen+1);
        new (&buf[ulen]) T(x);
        return buf[ulen++];
    }

    T &add()
    {
        if(ulen==alen) growbuf(ulen+1);
        new (&buf[ulen]) T;
        return buf[ulen++];
    }

    void add(const T &x, int n)
    {
        if(n <= 0) return;
        growbuf(ulen+n);
        loopi(n) new (&buf[ulen++]) T(x);
    }

    T &dup()
    {
        if(ulen==alen) growbuf(ulen+1);
        new (&buf[ulen]) T(buf[ulen-1]);
        return buf[ulen++];
    }

    void move(vector<T> &v)
    {
        if(!ulen)
        {
            swap(buf, v.buf);
            swap(ulen, v.ulen);
            swap(alen, v.alen);
        }
        else
        {
            growbuf(ulen+v.ulen);
            if(v.ulen) memcpy(&buf[ulen], (void  *)v.buf, v.ulen*sizeof(T));
            ulen += v.ulen;
            v.ulen = 0;
        }
    }

    bool inrange(size_t i) const { return i<size_t(ulen); }
    bool inrange(int i) const { return i>=0 && i<ulen; }

    T &pop() { return buf[--ulen]; }
    T &last() { return buf[ulen-1]; }
    T &first() { return buf[0]; }
    void drop() { ulen--; buf[ulen].~T(); }
    bool empty() const { return ulen==0; }

    int capacity() const { return alen; }
    int length() const { return ulen; }
    T &operator[](int i) { ASSERT(i>=0 && i<ulen); return buf[i]; }
    const T &operator[](int i) const { ASSERT(i >= 0 && i<ulen); return buf[i]; }

    void disown() { buf = NULL; alen = ulen = 0; }

    void shrink(int i) { ASSERT(i<=ulen); if(isclass<T>::no) ulen = i; else while(ulen>i) drop(); }
    void setsize(int i) { ASSERT(i<=ulen); ulen = i; }

    void deletecontents() { while(!empty()) delete   pop(); }
    void deletearrays() { while(!empty()) delete[] pop(); }

    T *getbuf() { return buf; }
    const T *getbuf() const { return buf; }
    bool inbuf(const T *e) const { return e >= buf && e < &buf[ulen]; }

    void growbuf(int sz)
    {
        int olen = alen;
        if(!alen) alen = max(MINSIZE, sz);
        else while(alen < sz) alen += alen/2;
        if(alen <= olen) return;
        uchar *newbuf = new uchar[alen*sizeof(T)];
        if(olen > 0)
        {
            if(ulen > 0) memcpy(newbuf, (void *)buf, ulen*sizeof(T));
            delete[] (uchar *)buf;
        }
        buf = (T *)newbuf;
    }

    databuf<T> reserve(int sz)
    {
        if(alen-ulen < sz) growbuf(ulen+sz);
        return databuf<T>(&buf[ulen], sz);
    }

    void advance(int sz)
    {
        ulen += sz;
    }

    void addbuf(const databuf<T> &p)
    {
        advance(p.length());
    }

    T *pad(int n)
    {
        T *buf = reserve(n).buf;
        advance(n);
        return buf;
    }

    void put(const T &v) { add(v); }

    void put(const T *v, int n)
    {
        databuf<T> buf = reserve(n);
        buf.put(v, n);
        addbuf(buf);
    }

    void remove(int i, int n)
    {
        for(int p = i+n; p<ulen; p++) buf[p-n] = buf[p];
        ulen -= n;
    }

    T remove(int i)
    {
        T e = buf[i];
        for(int p = i+1; p<ulen; p++) buf[p-1] = buf[p];
        ulen--;
        return e;
    }

    T removeunordered(int i)
    {
        T e = buf[i];
        ulen--;
        if(ulen>0) buf[i] = buf[ulen];
        return e;
    }

    template<class U>
    int find(const U &o)
    {
        loopi(ulen) if(buf[i]==o) return i;
        return -1;
    }

    void addunique(const T &o)
    {
        if(find(o) < 0) add(o);
    }

    void removeobj(const T &o)
    {
        loopi(ulen) if(buf[i] == o)
        {
            int dst = i;
            for(int j = i+1; j < ulen; j++) if(!(buf[j] == o)) buf[dst++] = buf[j];
            setsize(dst);
            break;
        }
    }

    void replacewithlast(const T &o)
    {
        if(!ulen) return;
        loopi(ulen-1) if(buf[i]==o)
        {
            buf[i] = buf[ulen-1];
            break;
        }
        ulen--;
    }

    T &insert(int i, const T &e)
    {
        add(T());
        for(int p = ulen-1; p>i; p--) buf[p] = buf[p-1];
        buf[i] = e;
        return buf[i];
    }

    T *insert(int i, const T *e, int n)
    {
        if(alen-ulen < n) growbuf(ulen+n);
        loopj(n) add(T());
        for(int p = ulen-1; p>=i+n; p--) buf[p] = buf[p-n];
        loopj(n) buf[i+j] = e[j];
        return &buf[i];
    }

    void reverse()
    {
        loopi(ulen/2) swap(buf[i], buf[ulen-1-i]);
    }
};

const int islittleendian = 1;

#endif
