const kick_gif = ['https://tenor.com/view/kung-fu-panda-karate-kick-gif-15261593','https://tenor.com/view/strong-kick-hammer-down-fatal-blow-scarlet-johnny-cage-gif-13863296'];
module.exports = {
	name: 'kick',
	description: 'Kicks a member',
    args: true,
    guildOnly: true,
    usage: "<member mention>",
	execute(message) {
        // Easy way to get member object though mentions.
        var member= message.mentions.members.first();
        // Kick
        member.kick().then((member) => {
            // Successmessage
            message.channel.send(":wave: " + member.displayName + " has been successfully kicked :point_right: \n" + kick_gifs[Math.floor(Math.random()*myArray.length)]);
        }).catch(() => {
            // Failmessage
            message.channel.send("Access Denied :stuck_out_tongue:");
        });
    }
};