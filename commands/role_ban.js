const ban_gif = ['https://imgur.com/V4TVpbC','https://tenor.com/view/thor-banhammer-discord-banned-banned-by-admin-gif-12646581','https://tenor.com/view/cat-red-hammer-bongo-cat-bang-hammer-gif-15733820'];
module.exports = {
	name: 'ban',
	description: 'Bans a member',
    args: true,
    guildOnly: true,
    usage: "<member mention>",
	execute(message) {
        // Easy way to get member object though mentions.
        var member= message.mentions.members.first();
        // Kick
        member.kick().then((member) => {
            // Successmessage
            
            message.channel.send(":wave: " + member.displayName + " has been successfully banned :point_right: \n" + ban_gifs[Math.floor(Math.random()*myArray.length)]);
        }).catch(() => {
            // Failmessage
            message.channel.send("Access Denied :stuck_out_tongue:");
        });
    }
};