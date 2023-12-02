#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include <curses.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <netinet/in.h>

__attribute__((constructor)) void ignore_me()
{
    setbuf(stdin, NULL);
    setbuf(stdout, NULL);
    setbuf(stderr, NULL);
}

int car_server_socket;
struct sockaddr_in server_addr;

void die()
{
    close(car_server_socket);
    endwin();
    exit(0);
}

void car_server_connect()
{
    printf("<<< -----------------------------------------------------------------------------\n");
    printf("<<< Connecting to local car server...\n");
    printf("<<< -----------------------------------------------------------------------------\n");
    car_server_socket = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP);
    server_addr.sin_family = AF_INET;
    server_addr.sin_port = htons(31337);
    server_addr.sin_addr.s_addr = inet_addr("127.0.0.1");
    printf("<<< Connected to local car server.\n");
    printf("<<< -----------------------------------------------------------------------------\n");
}

int send_command(char *cmd)
{
    printf("<<< Sending Command: %s\n", cmd);
    sendto(car_server_socket, cmd, 1, 0, (struct sockaddr *)&server_addr, sizeof(server_addr));
}

void driver_menu()
{
    initscr();
    keypad(stdscr, TRUE);
    nodelay(stdscr, TRUE);
    car_server_connect();
    char ch = 0, k = 0;
    printf("<<< -----------------------------------------------------------------------------\n");
    printf("<<< Use {w|a|s|d} to drive, E to exit. Make sure to press ENTER after each key!\n");
    printf("<<< -----------------------------------------------------------------------------\n");
    printf(">>> ");
    refresh();

    while (1)
    {
        ch = getch();
        switch (ch)
        {
        case 115:
            send_command("d");
            break;
        case 119:
            send_command("u");
            break;
        case 97:
            send_command("l");
            break;
        case 100:
            send_command("r");
            break;
        case 116:
            send_command("t");
            break;
        case 101:
        case 69:
            die();
            break;
        }
    }
}

void logo()
{
    printf("MMMMMMMMMMMMMMMMMMMMMMMMNKOxl:;'..            ...,:ldkKNWMMMMMMMMMMMMMMMMMMMMMMM\n");
    printf("MMMMMMMMMMMMMMMMMMMMNOdc,.                            .':oOXWMMMMMMMMMMMMMMMMMMM\n");
    printf("MMMMMMMMMMMMMMMMWKxc'                                      .:dKWMMMMMMMMMMMMMMMM\n");
    printf("MMMMMMMMMMMMMMXx:.             ...,;::ccccc:;,'..             .;xXWMMMMMMMMMMMMM\n");
    printf("MMMMMMMMMMMW0l.           .;cdk0XNWWMMMMMMMMWWNXKOdl;.           .l0WMMMMMMMMMMM\n");
    printf("MMMMMMMMMW0c.         .:dOXWMMMMMMMMMMMMMMMMMMMMMMMMWXOd:.         .c0WMMMMMMMMM\n");
    printf("MMMMMMMWKl.        .:xXWMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMWXkc.        .lKWMMMMMMM\n");
    printf("MMMMMMNx'        'dKWMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMWKd,        .xNMMMMMM\n");
    printf("MMMMMKc.       'dXMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMNk,        cKMMMMM\n");
    printf("MMMW0,       .oXMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMNx'       ,0WMMM\n");
    printf("MMWO'       ,OWMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMKc       'OWMM\n");
    printf("MMO'       :KMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMNd.      'OMM\n");
    printf("MK;       :XMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMWd.      ;KM\n");
    printf("Nl        .:oxOKNWMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMWX0kdl,.       lN\n");
    printf("k.             .':ldkKNWMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMWNKOxl:,..            .O\n");
    printf("c                    ..;cox0XWMMMMN0xdlllldx0NMMMMWX0koc;'.                    c\n");
    printf(".      ...                  .,:ldl,.        .,ldl:,..                 ...      .\n");
    printf("       lXKOdl:'.                                                .':ldkKXo       \n");
    printf("      .xMMMMMWNX0xoc;..                                  ..,:oxOKNWMMMMMk.      \n");
    printf("      .kMMMMMMMMMMMMWNKOdl:,.       Ret2Drive      .';cdk0XWMMMMMMMMMMMMO'      \n");
    printf("      .kMMMMMMMMMMMMMMMMMMWWX0d.                .cOKNWMMMMMMMMMMMMMMMMMMO.      \n");
    printf("      .dWMMMMMMMMMMMMMMMMMMMMMWo.               cXMMMMMMMMMMMMMMMMMMMMMMk.      \n");
    printf(".      cNMMMMMMMMMMMMMMMMMMMMMMNx'            'dNMMMMMMMMMMMMMMMMMMMMMMWo      .\n");
    printf(",      'OMMMMMMMMMMMMMMMMMMMMMMMMXx;        ;xXMMMMMMMMMMMMMMMMMMMMMMMMK;      ,\n");
    printf("o       cNMMMMMMMMMMMMMMMMMMMMMMMMMO.      .OMMMMMMMMMMMMMMMMMMMMMMMMMWd.      o\n");
    printf("0,      .xWMMMMMMMMMMMMMMMMMMMMMMMMO.      .OMMMMMMMMMMMMMMMMMMMMMMMMMO'      ,K\n");
    printf("Wx.      .kWMMMMMMMMMMMMMMMMMMMMMMMO.      .OMMMMMMMMMMMMMMMMMMMMMMMM0,      .xW\n");
    printf("MNl       .kWMMMMMMMMMMMMMMMMMMMMMMO.      .OMMMMMMMMMMMMMMMMMMMMMMW0,       lNM\n");
    printf("MMXc       .dNMMMMMMMMMMMMMMMMMMMMMO.      .OMMMMMMMMMMMMMMMMMMMMMWk'       cXMM\n");
    printf("MMMXl       .cKWMMMMMMMMMMMMMMMMMMMO.      .OMMMMMMMMMMMMMMMMMMMMXl.       lXMMM\n");
    printf("MMMMNo.       .dXMMMMMMMMMMMMMMMMMMO.      .OMMMMMMMMMMMMMMMMMMNx'       .oNMMMM\n");
    printf("MMMMMWk,        'dXWMMMMMMMMMMMMMMMO.      .OMMMMMMMMMMMMMMMWXx,        ,kWMMMMM\n");
    printf("MMMMMMMXl.        .lONMMMMMMMMMMMMMO.      .OMMMMMMMMMMMMMW0o'        .lKMMMMMMM\n");
    printf("MMMMMMMMW0c.        .,oONWMMMMMMMMMO.      .OMMMMMMMMMWNOo;.        .:0WMMMMMMMM\n");
    printf("MMMMMMMMMMW0c.          ':dOKNWMMMMO.      .OMMMMMNXOd:'.         .cOWMMMMMMMMMM\n");
    printf("MMMMMMMMMMMMWKo,            .':loxOo.      .oOxdl:,.            'o0WMMMMMMMMMMMM\n");
    printf("MMMMMMMMMMMMMMMNOl,.                                         'lONMMMMMMMMMMMMMMM\n");
    printf("MMMMMMMMMMMMMMMMMMN0d:'.                                 .:oONMMMMMMMMMMMMMMMMMM\n");
    printf("MMMMMMMMMMMMMMMMMMMMMWN0xl:'..                     .';ldOXWMMMMMMMMMMMMMMMMMMMMM\n");
    printf("MMMMMMMMMMMMMMMMMMMMMMMMMMWX0xl:'..           .';cdOXWMMMMMMMMMMMMMMMMMMMMMMMMMM\n");
}

void authenticate()
{
    char contact[16];
    printf("<<< -----------------------------------------------------------------------------\n");
    printf("<<< Remote Controlled CTF v4.1: Ret2Drive                                        \n");
    printf("<<< -----------------------------------------------------------------------------\n");
    printf("<<< We are sorry, but our car service is not available at this time. Please \n");
    printf("<<< provide your email contact info and we'll get back to you ASAP >>> ");
    fgets(contact, 32, stdin);
    printf("<<< Thank you!\n");
    return;
}

int main(int argc, char **argv)
{
    logo();
    authenticate();
    return 0;
}
