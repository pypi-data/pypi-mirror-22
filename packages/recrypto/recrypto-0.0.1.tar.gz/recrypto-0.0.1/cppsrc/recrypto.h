#ifndef RECRYPTO_CRYPTO_H
#define RECRYPTO_CRYPTO_H

#include <stdbool.h>

#ifdef __cplusplus
extern "C" {
#endif

void genprivkey(const char *seed, char **privstr, char **pubstr);
void genpubkey(const char *privstr, char **pubstr);
bool hashstring(const char *str, char *result, int maxlen);
void answerchallenge(const char *privstr, const char *challenge, char **answerstr);
void *parsepubkey(const char *pubstr);
void freepubkey(void *pubkey);
void *genchallenge(void *pubkey, const void *seed, int seedlen, char **challengestr);
void freechallenge(void *answer);
bool checkchallenge(const char *answerstr, void *correct);

#ifdef __cplusplus
}
#endif

#endif
