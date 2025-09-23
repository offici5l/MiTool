#!/bin/bash

API_URL="https://fce-api.onrender.com"

echo -e "\n=============================="
echo    "  Firmware Extractor CLI"
echo    "=============================="
echo -e "\nExtract files instantly from any ROM zip.\n"
echo -e "- Supported: boot.img (more coming soon)"
echo -e "- All boot.img files are also archived at:"
echo -e "    https://t.me/boot_img_zip\n"
echo -e "You can also use the website interface:"
echo -e "    https://fce-app.onrender.com"
echo -e "------------------------------\n"

read -p "Enter the firmware (.zip) URL: " ZIP_URL
IMAGE="boot.img"

RESPONSE=$(curl -s -X POST "$API_URL/extract" -H "Content-Type: application/json" -d "{\"url\":\"$ZIP_URL\", \"images\":\"$IMAGE\"}")

TASK_ID=$(echo "$RESPONSE" | grep -o '"task_id":"[^"]*' | cut -d':' -f2 | tr -d '"')
STATUS_URL=$(echo "$RESPONSE" | grep -o '"status_url":"[^"]*' | cut -d':' -f2- | tr -d '"')

if [[ -z "$TASK_ID" || -z "$STATUS_URL" ]]; then
    echo -e "\nFailed to start extraction: $RESPONSE\n"
    exit 1
fi

echo -e "\nTask started (Task ID: $TASK_ID)"
echo -n "Progress: "

LAST_STEP=""
LAST_MESSAGE=""
while true; do
    curl -s -X POST "$API_URL/heartbeat/$TASK_ID" > /dev/null

    STATUS_JSON=$(curl -s "$STATUS_URL")
    STATUS=$(echo "$STATUS_JSON" | grep -o '"status":"[^"]*' | cut -d':' -f2 | tr -d '"')
    MESSAGE=$(echo "$STATUS_JSON" | grep -o '"message":"[^"]*' | sed 's/"message":"//;s/"$//')
    DL_URL=$(echo "$STATUS_JSON" | grep -o '"download_url":"[^"]*' | sed 's/"download_url":"//;s/"$//')

    # Show all progress or error messages
    if [[ "$STATUS" == "failed" ]]; then
        STEP="$MESSAGE"
    else
        STEP=$(echo "$MESSAGE" | grep -o 'Step [0-9]\+/[0-9]\+' || echo "$MESSAGE")
        [[ "$STEP" == "" ]] && STEP="$MESSAGE"
    fi

    if [[ "$STEP" != "$LAST_STEP" || "$STATUS" == "completed" || "$STATUS" == "failed" ]]; then
        printf "\rProgress: %-40s" "$STEP"
        LAST_STEP="$STEP"
        LAST_MESSAGE="$MESSAGE"
    fi

    if [[ "$STATUS" == "completed" ]]; then
        echo -e "\rProgress: Completed!                                    \n"
        if [[ -n "$DL_URL" ]]; then
            echo -e "Done! Download link: $DL_URL\n"
        else
            echo -e "Extraction complete, but no download link found!\n"
        fi
        break
    elif [[ "$STATUS" == "failed" ]]; then
        echo -e "\rProgress: Failed!                                       "
        echo -e "\n$LAST_MESSAGE\n"
        echo "An error occurred during extraction!"
        echo
        break
    fi

    sleep 2
done