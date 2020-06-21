process.chdir('G:/My Drive/coding/node.js/bot')
const Discord = require('discord.js');
const bot = new Discord.Client();
const { prefix, TOKEN } = require('./cfg.json');
const fs = require('fs');
const cooldowns = new Discord.Collection();
bot.commands = new Discord.Collection();
const commandFiles = fs.readdirSync('./commands/').filter(file => file.endsWith('.js'));
for (const file of commandFiles) {
	const command = require(`./commands/${file}`);
	// set a new item in the Collection
	// with the key as the command name and the value as the exported module
	bot.commands.set(command.name, command);
}




bot.on('ready', () => {
    console.info(`Logged in as ${bot.user.tag}!`);
});

bot.on('message', message => {
    if (message.content.startsWith(prefix)){
        const args = message.content.slice(prefix.length).split(/ +/);
        if (!args) {
            console.log('cannot process command.');
            return message.channel.send('Failed to process the command!')
        }
        const commandName = args.shift().toLowerCase();
        const command = bot.commands.get(commandName)
            || client.commands.find(cmd => cmd.aliases && cmd.aliases.includes(commandName));
        if (!command) return;
        try{
            if (command.guildOnly && message.channel.type !== 'text') {
                return message.reply('I can\'t execute that command inside DMs!');
            }            
            if (command.args && !args.length) {
                let reply = `You didn't provide any arguments, ${message.author}!`;
                if (command.usage) {
                    reply += `\nThe proper usage would be: \`${prefix}${command.name} ${command.usage}\``;
                }
                return message.channel.send(reply);
            }
        } catch {
            console.log('Command not found????');
            return message.channel.send('Command not found. try prefix `/`,`!` or `;`.');
        }
        if (!cooldowns.has(command.name)) {
            cooldowns.set(command.name, new Discord.Collection());
        }
        const now = Date.now();
        const timestamps = cooldowns.get(command.name);
        const cooldownAmount = (command.cooldown || 1) * 1000;
        if (timestamps.has(message.author.id)) {
            const expirationTime = timestamps.get(message.author.id) + cooldownAmount;
            if (now < expirationTime) {
                const timeLeft = (expirationTime - now) / 1000;
                return message.reply(`please wait ${timeLeft.toFixed(1)} more second(s) before reusing the \`${command.name}\` command.`);
            }
        }
        timestamps.set(message.author.id, now);
        setTimeout(() => timestamps.delete(message.author.id), cooldownAmount);
        try {
	        command.execute(message, args);
        } catch (error) {
	        console.error(error);
            message.reply('there was an error trying to execute that command!');
        return;
        }
    }else{
        if (message.content.toLowerCase() === "what?"){
            message.react('687109358248525853');
            return;
        }
        if (message.content.toLowerCase() === 'wat?'){
            message.channel.send('Say what?');
            return;
        }
        if (message.content.toLowerCase() === 'vincidiot'){
            message.channel.send('Vinci is an idiot!');
            return;
        }
        if (message.content.toLowerCase() === 'benz'){
            message.channel.send('Stupid benz is a sucker and a noob!');
            return;
        }
        if (message.content.toLowerCase() == 'siriustupid'){
            message.channel.send('Sirius is so so stupid!');
            return;
        }
    }

});



bot.login(TOKEN);