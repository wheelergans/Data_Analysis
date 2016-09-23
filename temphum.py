#temp and humidity
title = 'Humidity and Temperature '
ax = pow_data[['temp','hum']].plot(title = title,secondary_y =['hum'],linewidth =2,grid = True)
ax.set_ylabel('temp (C)')
ax.right_ax.set_ylabel('Hum')
ax.set_xlabel('')

#ax.axhline(means['temp'],color = 'blue',lw=2,linestyle = '--')
#ax.right_ax.axhline(means['hum'],color = 'green',lw=2,linestyle = '--')

lgd = ax.legend(loc='upper left', bbox_to_anchor=(1, 1))

plt.savefig(title, bbox_extra_artists=(lgd,), bbox_inches='tight')