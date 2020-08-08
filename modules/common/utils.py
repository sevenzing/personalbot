import logging

def get_logger(name='bot'):
    return logging.getLogger(name)

#%%
def parse_commad(text: str):
    '''
    Takes text of telegram message, 
    parses it into command and arguments 
    
    Returns tuple: (command, [arguments,])
    '''
    command, _, raw_args = text.partition(' ')
    sep = ',' if ',' in raw_args else '\n' if '\n' in raw_args else ' '
    args = list(
        map(lambda x: x.strip(), 
            filter(lambda x: x != '', raw_args.split(sep))
        )
    )
    return (command, args)



# %%
